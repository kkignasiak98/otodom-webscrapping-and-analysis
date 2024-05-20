from bs4 import BeautifulSoup
import pandas as pd
from requests import get


class OtoDomDataExtractor:
    def __init__():
        pass


# Funkcja `extract_pages` pobiera informacji z wskazanych stron.
@staticmethod
def extract_pages(
    baseURL: str, start: int, end: int, patterns: list[str]
) -> pd.DataFrame:
    """
    Extracts data from multiple pages of the website
    and concatenates them into a single DataFrame.
    Parameters:
        baseURL (str): The base URL for the pages to be extracted.
        start (int): The starting page number.
        end (int): The ending page number.
        patterns (list): A list of patterns to search for in each page.
    Returns:
        pandas.DataFrame: The concatenated DataFrame containing the extracted data.
    """
    main_df = pd.DataFrame(columns=patterns)
    for x in range(start, end):  # iterate through the selected pages
        URL = baseURL + str(x)
        page = get(URL)
        bs = BeautifulSoup(page.content, "html.parser")
        df = extract_page(bs, patterns)
        frames = [main_df, df]
        main_df = pd.concat(frames)
    main_df.drop_duplicates()  # removal of ads that appeared on more than one page
    return main_df


@staticmethod
def extract_page(page: str, patterns: list[str]) -> pd.DataFrame:
    """
    Extracts data from a single page of the website
    and concatenates it into a single DataFrame.

    Parameters:
        page (str): The page content to extract data from.
        patterns (list[str]): A list of patterns to search for in the page.

    Returns:
        pd.DataFrame: The concatenated DataFrame containing the extracted data.
    """
    links = []
    links = get_links(
        page
    )  # downloading all links from the site directing to individual listings
    main_df = pd.DataFrame(columns=patterns)
    for link in links:
        df = get_subpage_information(
            link, patterns
        )  # downloading all data about a particular offer
        frames = [main_df, df]
        main_df = pd.concat(frames)
    return main_df


@staticmethod
def get_links(page) -> list[str]:
    """
    Extracts links from a given webpage leading to offers.

    Parameters:
        page (BeautifulSoup): The BeautifulSoup object representing the webpage.

    Returns:
        list: A list of links found on the webpage.
    """
    links = []
    offers = page.find_all("div", class_="offer-item-details")
    for offer in offers:
        link_area = offer.find("h3")
        link_info = link_area.find("a")
        link = link_info.get("href")
        links.append(link)
    return links


@staticmethod
def get_subpage_information(link: str, patterns):
    """
    This function is used to ectract data about a single offer.

    Parameters:
        link,
        patterns: (list[str]): A list of patterns to search for in the page.

    Returns:
        list: A pandas DataFrame containing the extracted information from the subpage.
    """
    page = get(link)
    bs_sub = BeautifulSoup(page.content, "html.parser")
    details = get_details(bs_sub)
    df = details_to_df(details, patterns)
    return df


@staticmethod
def get_details(page) -> list:
    """
    A function to extract details from a webpage.

    Parameters:
        page: BeautifulSoup object - the webpage to extract details from.

    Returns:
        list - a list of details extracted from the page.
    """
    details = []
    details_area = page.find("div", class_="css-1d9dws4 egzohkh2")
    details_info = details_area.find_all("div", class_="css-18h1kfv ev4i3ak3")

    for detail_info in details_info:
        detail = detail_info.text
        details.append(detail)
    price = get_price(page)
    price = wrap_price(price)
    details.append(price)
    return details


@staticmethod
def get_price(page) -> str:
    """
    A function to get the price information from a BeautifulSoup page.

    Parameters:
        page: BeautifulSoup object - the webpage to extract the price from.

    Returns:
        str - the price extracted from the page.
    """
    price_info = page.find("strong", class_="css-srd1q3 eu6swcv17")
    price = price_info.text

    return price


@staticmethod
def wrap_price(price) -> str:
    """
    A function to wrap the price with additional text " Cena".

    Parameters:
        price : str - the price to be wrapped.

    Returns:
        str - the wrapped price.
    """
    price = price + " Cena"
    return price


def details_to_df(details: list, patterns: list) -> pd.DataFrame:
    """
    A function to convert details into a DataFrame based on specified patterns.

    Parameters:
        details: list - a list of details to process.
        patterns: list - a list of patterns to search in the details.

    Returns:
        pandas.DataFrame - the DataFrame created from the details based on the patterns.
    """
    values = []
    for pattern in patterns:
        founded = 0
        for item in details:
            if pattern in item:
                founded = 1
                item = item.replace(pattern, "")
                values.append(item)
        if founded == 0:
            values.append(-1)

    df = pd.DataFrame(values)
    df = pd.DataFrame.transpose(df)
    df.columns = patterns

    return df
