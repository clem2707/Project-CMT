from algorithms.map import map
# from algorithms.predictions import pred
# from algorithms.display import show

def main():
    data_path = "./data/raw/"

    map("./data/raw/harbor.csv" , './data/processed/interior_points.csv', "./results/lake_map.png")
    # pred()
    # show()

if __name__ == "__main__":
    main()