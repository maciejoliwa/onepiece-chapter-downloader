from models import Chapter

import os.path
import click
import bs4
import typing as tp
import requests


BASE_URL = 'https://readonepiece.in/manga/one-piece-chapter-'


def get_one_piece_chapter(number: tp.Union[str, int]) -> Chapter:
    response = requests.get(f"{BASE_URL}{number}")
    content = response.content

    page = bs4.BeautifulSoup(content, 'html.parser')
    chapter = Chapter(number, [], "")

    chapter.images = [link.attrs['src'] for link in page.select('.entry-content img')]
    return chapter


@click.command()
@click.argument('number')
@click.option('--save', default='', help='Path to save the chapter to')
def main(number: str, save: str) -> None:
    if not os.path.exists(save):
        raise Exception("Path does not exist")
        
    chapter = get_one_piece_chapter(number)
    chapter.save(save)

    print("done!")


if __name__ == '__main__':
    main()
