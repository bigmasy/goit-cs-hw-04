import os
from faker import Faker
def create_test_files(directory, num_files, keywords):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    fake = Faker()
    
    for i in range(num_files):
        file_path = os.path.join(directory, f"file{i+1}.txt")
        with open(file_path, 'w') as f:
            content = fake.text(max_nb_chars=200)
            if i % 2 == 0:  # Додати ключове слово у кожний другий файл
                keyword = keywords[i % len(keywords)]
                content += f" {keyword}"
            f.write(content)
    print(f"Created {num_files} test files in {directory}")

if __name__ == "__main__":
    directory = "test_files"
    num_files = 50
    keywords = ["keyword1", "keyword2", "keyword3"]
    
    create_test_files(directory, num_files, keywords)
