import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_gene_info_by_gene_number(gene_numbers):
    data = []

    number_list = gene_numbers.split(',')
    for number in number_list:
        url = f"https://www.ncbi.nlm.nih.gov/gene/{number}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        word_element = soup.find('dd', class_='noline')
        word = word_element.contents[0] if word_element else "Not Found"
        sp_element = soup.find('dd', class_='tax')
        sp = sp_element.find('a').contents[0] if sp_element else "Not Found"

        data.append([number, word, sp, url])

    df = pd.DataFrame(data, columns=['gene', 'gene_name', 'sp', 'url'])
    return df

def get_gene_info_by_gene_name(gene, species=None):
    data = []

    if species is None:
        url = f"https://www.ncbi.nlm.nih.gov/gene/?term={gene}"
    else:
        sp1, sp2 = species.split(' ')
        url = f"https://www.ncbi.nlm.nih.gov/gene/?term={sp1}+{sp2}+{gene}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    gene_elements = soup.find_all('td', class_='gene-name-id')
    for gene_element in gene_elements:
        gene_name = gene_element.a.get_text()
        number_element = gene_element.find_next('span', class_='gene-id')
        gene_number = number_element.get_text() if number_element else "Not Found"
        species_element = gene_element.find_next('td').find_next('em')
        species_name = species_element.get_text() if species_element else "Not Found"

        if species is None:
            data.append([gene_name, species_name, gene_number, url])
        else:
            data.append([gene_name, species_name, gene_number, url])
            break  # Break the loop after finding the first entry for the specified species

    df = pd.DataFrame(data, columns=['gene_name', 'sp', 'id', 'url'])
    return df

def get_gene_info_by_rsid(rsid):
    data = []
    url = f"https://www.ncbi.nlm.nih.gov/snp/{rsid}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sp = soup.find('dd', class_='species_name').contents[0]
    gene_dd = soup.find_all('dl', class_='usa-width-one-half')[1].find_all('dd')[1]
    gene_element = gene_dd.find('span') if gene_dd else None
    gene = gene_element.get_text() if gene_element else "Not Found"

    data.append([rsid, sp, gene, url])

    df = pd.DataFrame(data, columns=['rsid', 'sp', 'gene:variant type', 'link'])
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve gene information.")
    parser.add_argument("gene_info", nargs="+", help="Gene name, or gene name and species, gene numbers (comma-separated) or rsid")
    args = parser.parse_args()

    gene_info = " ".join(args.gene_info)

    if gene_info.isdigit():
        result_df = get_gene_info_by_gene_number(gene_info)
    elif gene_info.startswith('rs'):
        result_df = get_gene_info_by_rsid(gene_info)
    else:
        gene_info_parts = gene_info.split(' ')
        gene_name = gene_info_parts[0]
        species = " ".join(gene_info_parts[1:]) if len(gene_info_parts) > 1 else None
        result_df = get_gene_info_by_gene_name(gene_name, species)

    print(result_df)
