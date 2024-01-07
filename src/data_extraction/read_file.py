

if __name__ == "__main__":
    f = open("./data/data.jsonl", "r")
    lines = f.readlines() 
    stripped_lines = [line.strip() for line in lines]
    print(stripped_lines)
    joined_lines = (',').join(stripped_lines)
    print(joined_lines)
    with open('json_data.json', 'w') as f: 
        f.write(joined_lines)
