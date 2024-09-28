from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import uuid


def format_response(response: str):
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-3.5-turbo",
        "usage": {
            "prompt_tokens": 10,  # Hardcoded value
            "completion_tokens": len(response.split()),
            "total_tokens": 10 + len(response.split())
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }

class gptParser:
    def __init__(self, driver, gpt_url: str = 'https://chat.openai.com/'):
        self.driver = driver
        self.driver.get(gpt_url)
        self.history = []

    @staticmethod
    def get_driver():
        uc.TARGET_VERSION = 124
        return uc.Chrome()

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )
        input_field.send_keys(msg)
        
        # Find and click the send button
        send_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
        send_button.click()
        
        # Wait for the response to load
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".markdown"))
        )
        
        # Update history
        self.update_history()

    def update_history(self):
        try:
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, ".markdown")
            self.history = [ele.text for ele in all_elements]
        except:
            self.history = []

    def read_respond(self):
        try:
            return self.history[-1] if self.history else None
        except:
            return None

    def new_chat(self):
        new_chat_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/"]'))
        )
        new_chat_button.click()

    def close(self):
        self.driver.quit()

def ask_gpt_for_final_answer_old(gpt_parser, question, answer_one, answer_two):
    query = f"There is a farmer asking about a question. The question is: {question} This is the first answer: {answer_one} And this is the second answer: {answer_two} If you are a botanist, tell me which one is more precise."
    print("Query:", query)
    print("=====")

    gpt_parser(query)
    time.sleep(10)  # Increased wait time
    response = gpt_parser.read_respond()
    
    if response:
        print("ChatGPT Response:")
        print(response)
        time.sleep(10)
        return format_response(response)
    else:
        print("No response received from ChatGPT.")
    print("==========")
    return format_response("No response received from ChatGPT.")

def ask_gpt_for_final_answer(gpt_parser, query):
    print("Query:", query)
    print("=====")

    gpt_parser(query)
    time.sleep(10)  # Increased wait time
    response = gpt_parser.read_respond()
    
    if response:
        print("ChatGPT Response:")
        print(response)
        time.sleep(10)
        return format_response(response)
    else:
        print("No response received from ChatGPT.")
    print("==========")
    return format_response("No response received from ChatGPT.")
    
    # gpt_parser.close()

if __name__ == "__main__":
    
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)
    
    question = "What is Anthracnose caused by?"
    
    answer_one = "A classic reference! According to Ocfemia, GO, Agati JA (1925), anthracnose is caused by the fungus Colletotrichum lagenarium."

    answer_two = "Anthracnose is a fungal disease caused by various species of the genus Colletotrichum. The pathogen that causes anthracnose depends on the host plant and region. In some hosts or regions, a dominant Colletotrichum species may be responsible for the disease. In hosts such as coffee, citrus, and strawberries, the disease is often caused by Colletotrichum spp. such as C. kahawae, C. acutatum, and C. fragariae, respectively. In regions where the boniense clade is present, the disease is typically caused by Colletotrichum boniense. This clade is characterized by a specific set of morphological and molecular features. The boniense clade is widespread and has been reported to cause anthracnose in various hosts, including coffee, citrus, and other crops. It is considered a major threat to agriculture, as it can cause significant yield loss and reduce crop quality. In regions where the boniense clade is present, it is often the dominant cause of anthracnose, and its presence can have significant implications for disease management and crop protection strategies. It's worth noting that the boniense clade is not the only clade that can cause anthracnose, and other clades, such as the lindemuthianum and dematium clades, can also be responsible for the disease in different hosts and regions."
    
    ask_gpt_for_final_answer(gpt_parser, question, answer_one, answer_two)
    
    question = "What causes Downy Mildew?"

    answer_one = "According to Smith and Jones (1898), downy mildew is caused by the water mold Plasmopara viticola, which primarily affects grapevines."

    answer_two = (
        "Downy mildew is caused by various species of water molds, also known as oomycetes, "
        "depending on the host plant. Plasmopara viticola is the most common pathogen associated with "
        "downy mildew in grapevines. However, in other plants, such as lettuce, cucumbers, and spinach, "
        "different species are involved. For example, Bremia lactucae is the main causal agent in lettuce, "
        "while Peronospora cubensis causes downy mildew in cucumbers. These pathogens thrive in moist, cool conditions, "
        "where they infect leaves and cause characteristic yellow spots or patches. Downy mildew can be managed by improving air "
        "circulation around plants, using resistant cultivars, and applying fungicides as necessary."
    )  
    ask_gpt_for_final_answer(gpt_parser, question, answer_one, answer_two)
    
    gpt_parser.close()