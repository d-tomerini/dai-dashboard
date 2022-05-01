import asyncclick as click
import pandas as pd
from bs4 import BeautifulSoup
import logging
import httpx
import re
from scrape_and_visualize.models.pydanticmodels import Runner
from scrape_and_visualize.models.database import DB_Runner
from scrape_and_visualize.services.database import engine, Base, Session

fh = logging.FileHandler('logs.txt')
fh.setLevel(logging.ERROR)

sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(sh)

def list_alphabet():
    for i in range(ord('a'), ord('z') + 1):
        yield chr(i)

def click_year_param_validate(s,e):
    if s >= e:
        raise click.BadParameter(f"Start year {s} and end_year {e}: in empty set")
    return


@click.command()
@click.option('--start-year', '-s', default=2014,  type=int, help='Start year to use')
@click.option('--end-year', '-e', default=2019,  type=int, help='Search up to this year (excluded)')
async def scrape(start_year, end_year):
    runners = []
    pages_not_parsed = []
    runners_not_parsed = 0

    click_year_param_validate(start_year, end_year )

    regex = re.compile('([\d\?]{4}) ([\D\s]+) ([\d:,.-]+)', re.U)

    async with httpx.AsyncClient() as client:
        for year in range(start_year, end_year):
            for letter in list_alphabet():
                marathon_url = f'https://services.datasport.com/{year}/lauf/zuerich/alfa{letter}.htm'
                response = await client.get(marathon_url)

                if response.status_code == 200:
                    logging.info(f"url {marathon_url} processed correctly")
                else:
                    logging.warning(f"url returned code {response.status_code}")
                    pages_not_parsed.append(marathon_url)
                    continue

                # Parsing the HTML
                soup = BeautifulSoup(response.content, 'html.parser')

                for myds in soup.find_all("span", attrs={'class': 'myds'}):
                    info = myds.parent.contents[0]
                    try:
                        match = regex.search(myds.parent.contents[2])
                        runner = Runner(
                            Fullname=myds.text,
                            Category=info.split()[0],
                            Rang=info.split()[1],
                            Age_year=match.group(1),
                            Location=match.group(2),
                            total_time=match.group(3),
                            run_link=marathon_url,
                            run_year=year
                        )
                        runners.append(runner)
                    except Exception as e:
                        logging.warning('e')
                        logging.warning(f"Couldn't parse runner at line {info}")
                        runners_not_parsed += 1

    if runners_not_parsed > 0:
        logging.warning(f'Could not parse {runners_not_parsed} runners')
    else:
        logging.warning(f"All runners processed")
    if len(pages_not_parsed) > 0:
        logging.warning(f'Could not parse {len(pages_not_parsed)}')
        for page in pages_not_parsed:
            logging.warning(page)
    else:
        logging.info("All urls processed")
    logging.info(f'Processed {len(runners)} runners')
    if len(runners) == 0:
        logging.warning("The search did not find any runner")
        exit(0)

    runners_df = pd.DataFrame([dict(p) for p in runners])
    runners_df.Age_year = runners_df.Age_year.astype('Int64')

    Base.metadata.create_all()
    runners_df.to_sql("runners", engine, if_exists='append', index=False)


if __name__ == '__main__':
    scrape(_anyio_backend="asyncio")
    with Session() as session:
        q = session.query(DB_Runner.Age_year).count()
        print(q)
