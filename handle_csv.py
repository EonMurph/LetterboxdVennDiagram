from csv import writer as csv_writer


def save_to_csv(movies: dict[str, list[str]], filename: str):
    with open(filename, 'w', newline='') as out_file:
        writer = csv_writer(out_file)
        writer.writerow(['Name', 'Year', 'URL'])
        for movie in movies:
            writer.writerow([movie[0], movie[1], movie[2]])
