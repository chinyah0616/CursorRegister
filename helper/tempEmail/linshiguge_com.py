import time
from DrissionPage import ChromiumOptions, Chromium

class Linshigugecom:

    LINSHIGUGE_COM_URL = "https://www.linshiguge.com/"

    def __init__(self, browser: Chromium):
        self.tab = browser.new_tab(self.LINSHIGUGE_COM_URL)
        self.email_address = None
        self.retry_times = 5

        self.tab.wait(5)

        for retry in range(self.retry_times):
            try:
                shadow_root_1 = self.tab.ele('@id=NOic5').child().child().shadow_root
                shadow_root_2 = shadow_root_1.ele("tag:iframe", timeout=30).ele("tag:body").shadow_root
                button = shadow_root_2.ele("xpath=//input[@type='checkbox']")
                button.click()

            except Exception as e:
                pass

            self.tab.wait(0.5, 1)
            if self.tab.wait.eles_loaded("xpath=//input[@id='active-mail']", timeout=5):
                break

            if retry == self.retry_times -1:
                print("[linshiguge.com] Fail to bypass Cloudflare.")
        
    def get_email_address(self):

        for retry in range(self.retry_times):            
            try:
                # If the email already has the message, get a new one
                self.tab.ele("xpath=//a[@id='newMailbox']").click()
                self.tab.wait(5)

                #if self.tab.wait.eles_loaded("xpath=//div[@class='base-layout-root']", timeout=5):
                #    self.tab.ele("xpath=//a[@id='newMailbox']").click()

                # Wait until the new email generated
                for retry in range(self.retry_times):
                    self.tab.wait(2.5, 4.5)
                    self.email_address = self.tab.ele("xpath=//input[@id='active-mail']").value
                    if "@" in self.email_addres:
                        return self.email_address 
            except:
                pass
               
            if retry == self.retry_times -1:
                print("[linshiguge.com] Fail to get email.")

        if self.email_address is None:
            print("[linshiguge.com] Fail to get email address from linshiguge.com")
            return None
        
        return self.email_address
        
    def wait_for_message(self, delay=5, timeout=300):
        delay = max(delay, 5)

        start_time = time.time()
        while time.time() - start_time <= timeout:

            try:
                self.tab.wait(delay)

                self.tab.refresh()
                messages = self.tab.ele("xpath=//tbody[@id='message-list']")
                message_trs = messages.children()
                if len(message_trs) > 0:
                    message_curor = [message_tr.children()[0] for message_tr in message_trs if message_tr.children()[0].text.lower() == "cursor"]
                    if len(message_curor) > 0:
                        message_curor = message_curor[0]
                        message_curor.child().click()
                        self.tab.wait(1.5, 3.5)

                        content = self.tab.ele("xpath=//div[@class='base-layout-root']")

                    return {
                        "text": content.text
                    }

            except Exception as e:
                pass

        return None

if __name__ == "__main__":

    options = ChromiumOptions()
    options.auto_port()
    # Use turnstilePatch from https://github.com/TheFalloutOf76/CDP-bug-MouseEvent-.screenX-.screenY-patcher
    options.add_extension("../../turnstilePatch")

    browser = Chromium(options)
    a = Linshigugecom(browser=browser)
    address = a.get_email_address()
    print(address)
    a.wait_for_message()
    
