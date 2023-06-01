" This module for Scraping Products from www.amazon.in "
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Prakash bhatiya                           #
#   Date: 24/05/2023                                #
#   Desc: Scraping Amazon Details                   #
#   Email: bhatiyaprakash991@gmail.com              #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
from utils import save_response
import os, json, time
from  bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class Amazon:
    """Class of amazon
    """
    # >> just for decoration
    def intro(self):
      print()
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print('  #                                        #')
      print('  #     SCRAPER FOR Amazon Products        #')
      print('  #           By: PRAKASH BHATIYA          #')
      print('  #             Dt: 24-05-2023             #')
      print('  #      bhatiyaprakash991@gmail.com       #')
      print('  #                                        #')
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print()

    def header(self, type: str) -> dict:
        """This method requests headers

        Args:
            type (str): String

        Returns:
            dict: dictionery format data
        """
        if type == 'product_url':
            {
            'authority': 'www.amazon.in',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en;q=0.7',
            'cookie': 'session-id=261-1522618-0333048; ubid-acbin=262-9412164-3300840; i18n-prefs=INR; lc-acbin=en_IN; session-id-time=2082787201l; csm-hit=adb:adblk_yes&t:1682421662541&tb:16H2CDJYR36KTKQGFMS5+s-93A4RZ68J6BX3HARGS8G|1682421662541; session-token=TJtT2lMb8OdsP3ECIbd2v3krUIHPRw16l30ckELX+LP4Eh4sCcbxhPwpUU+ZnyqvDxCL8uQZOfIwf9Ha++9f8701dnWC5dGQTnirl9yZEdMwtY20c66qTapHGcptjaZ4VHW6MGgNCVEDYOcSy46bNXWA7wlTPzL18BhIRMdtqYaqz/wcBvHkcnSragJ8BXF89j4ef1IOAON+ZY79pperKoIkf+R61ctmVDpGI1wbDeM=; i18n-prefs=INR; lc-acbin=en_IN; session-id=257-5973219-9388640; session-id-time=2082787201l; session-token="N5MPfCmsK9pLvL2RsVjkUljwouhEwF3hgj+CiaoFHK3beGF2J431ojdhGJaorZ8vH3hWkBsz2I2FrteMRZ6V998X3Exj5mkVXPoWjfsnRknqNjPyTG4ZwPe9daHGvJ9grojuxSSfmoZUmJEMm74fbZGl48T5caN91Os1QiW3BrMh+ZfTz/kbGup1d9amOauU5Hpz4HvmfD+D6t+TIDe6ofiPYQZ6N78JtZmrL8F6Pew="; ubid-acbin=260-9160758-8020857',
            'referer': 'https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        else:
            return {
            'Cookie': 'i18n-prefs=INR; session-id=257-5973219-9388640; session-id-time=2082787201l; session-token="GftjYkmvedUdZOeFqr9mvbKA91HIN3Zf86DiAZuzP4X30LYHozpsh7pppqd3mZZXLjgV3w1vFaXwzWqEccf6WD69CjejTZoL3UuK0FWBGF8g/zRMQTJ/W0brXzOyY1Yj+dZmVyk8qt3iFfcWmA3rTjisvZVFoZp0w2KQlel0wCaNRyW6Cf7s9T9teX3HHs2sIqHSjKOXrxoqggCN6p4XpfsA4DKg9oEflMH4n5pWoIk="; ubid-acbin=260-9160758-8020857'
            }

    def get_category(self) -> None:
        """This method get categories
        """
        categories = []

        json_path = os.path.join(os.path.dirname(__file__), "Data/amazon/")
        with open(os.path.join(json_path, "category.html"), "r", encoding="utf-8") as category:
            text = category.read()
        soup = BeautifulSoup(text)
        uls = soup.find_all("ul")
        category_list = []
        for ul in uls:
            id = ul.get("data-menu-id")
            if not int(id) > 7 :
                continue
            category = ul.find_all('div')

            for cat in category:
                sub_category = []
                if "main menu" in cat.text.strip():
                    continue
                title_li = cat.parent
                while True:
                    next_sib = title_li.find_next_sibling("li")
                    if next_sib.find("a"):
                        url = next_sib.find('a').get("href")
                        try:
                            node = url.split("node=")[1].split("&")[0]
                        except Exception:
                            break
                        product_url = f"https://www.amazon.in/s?rh=n%3A{node}&fs=true&ref=lp_{node}_sar"
                        sub_category.append({
                            "name": next_sib.find('a').text.strip(),
                            "url": url,
                            "product_list_url": product_url,
                            "product": []
                        })
                        title_li = next_sib
                    else: break
                category_list.append({
                    "category": cat.text.strip(),
                    "sub_category": sub_category
                })
        categories.append(category_list)
        save_response(categories, "category_list.json", "Data/amazon/")

    def get_asincode(self) -> None:
        """ Thie method to get asincode from url
        """
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        json_path = os.path.join(os.path.dirname(__file__), "Data/amazon/")
        with open(os.path.join(json_path, "category_list.json"), "r", encoding="utf-8") as category:
            data = json.load(category)
        # >> Add items in category list
        for i in data:
            for j in i:
                count = 0
                for k in j['sub_category']:
                    if k['product']:
                        continue
                    page = context.new_page()
                    page.goto(k['product_list_url'])
                    time.sleep(4)
                    if count == 4:
                        break
                    count += 1
                    url = page.query_selector_all("xpath=//h2/a[contains(@class, 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')]")
                    count2 = 0
                    asin_list = []
                    for u in url[4:]:
                        href = u.get_attribute('href')
                        if count2 == 4:
                            break
                        count2 += 1
                        try:
                            asincode = href.split('dp%2F')[1].split('%2F')[0]
                        except Exception:
                            asincode = href.split('/dp/')[1].split('/ref')[0]
                        asin_list.append({
                            "title": u.inner_text(),
                            "asin_code": asincode,
                            "details": []
                        })
                    k['product'] = asin_list
                    save_response(data, "category_list.json", "Data/amazon/")
                    page.close()
        browser.close()

    def get_product_details(self, asincode: str) -> list:
        """ This method to get product details by passing asincode

        Args:
            asincode (str): string

        Returns:
            list: list of data
        """
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        product_list = []
        # >> Add items in category list
        product_url = f"https://www.amazon.in/dp/{asincode}"
        page2 = context.new_page()
        page2.goto(product_url)
        time.sleep(4)
        # >> Getting product details
        try:
            title = page2.query_selector("xpath=//span[contains(@id, 'productTitle')]").inner_text()
        except Exception:
            page2.close()
            return
        try:
            image_link = page2.query_selector_all("xpath=//span[contains(@class, 'a-button-text')]//img")
            image_urls = []
            for x in image_link:
                image_urls.append(x.get_attribute('src'))
        except Exception:
            image_urls = []
        try:
            shop_name = page2.query_selector("xpath=//div[contains(@id, 'bylineInfo')]//a").inner_text()
        except Exception:
            shop_name = None
        try:
            total_rating = page2.query_selector("xpath=//span[contains(@id, 'acrCustomerReviewText')]").inner_text()
        except Exception:
            total_rating = None
        try:
            emi = page2.query_selector("xpath=//div[contains(@id, 'inemi_feature_div')]//span").inner_text()
        except Exception:
            emi = None
        try:
            no_cost_emi = page2.query_selector("xpath=//div[contains(@id, 'itembox-NoCostEmi')]//span[contains(@class, 'a-truncate a-size-base')]").inner_text()
        except Exception:
            no_cost_emi = None
        try:
            bank_offer = page2.query_selector("xpath=//div[contains(@id, 'itembox-InstantBankDiscount')]//span[contains(@class, 'a-truncate a-size-base')]").inner_text()
        except Exception:
            bank_offer = None
        try:
            partner_offer = page2.query_selector("xpath=//div[contains(@id, 'itembox-Partner')]//span[contains(@class, 'a-truncate a-size-base')]").inner_text()
        except Exception:
            partner_offer = None
        offer = {
            "no_cost_emi": no_cost_emi,
            "bank_offer": bank_offer,
            "partner_offer": partner_offer
        }
        try:
            price = page2.query_selector("xpath=//span[contains(@class, 'a-price-whole')]").inner_text()
        except Exception:
            price = None
        try:
            star_rating = page2.query_selector("xpath=//i[contains(@class, 'a-icon a-icon-star a-star-4 cm-cr-review-stars-spacing-big')]").inner_text()
        except Exception:
            star_rating = None
        try:
            delivery = page2.query_selector("xpath=//div[contains(@class, 'a-spacing-base')]//a").inner_text()
        except Exception:
            delivery = None
        try:
            date = page2.query_selector("xpath=//div[contains(@class, 'a-spacing-base')]//span//span").inner_text()
        except Exception:
            date = None
        try:
            status = page2.query_selector("xpath=//span[contains(@class, 'a-size-medium a-color-success')]").inner_text()
        except Exception:
            status = None
        try:
            add_protection_plan = page2.query_selector("xpath=//label[contains(@for, 'mbb-offeringID-1')]").inner_text()
        except Exception:
            add_protection_plan = None
        try:
            quantity = page2.query_selector("xpath=//span[contains(@id, 'a-autoid-2-announce')]//span[contains(@class, 'a-dropdown-prompt')]").inner_text()
        except Exception:
            quantity = None
        try:
            spec_table = page2.query_selector_all("xpath=//table[contains(@id, 'productDetails_techSpec_section_1')]//tr")
            specs = []
            for row in spec_table:
                specs.append({
                    "key": row.query_selector("xpath=//th").inner_text().strip(),
                    "value": row.query_selector("xpath=//td").inner_text().strip()
            })
        except Exception:
            specs = None
        try:
            add_info_table = page2.query_selector_all("xpath=//table[contains(@id, 'productDetails_detailBullets_sections1')]//tr")
            addi_info = []
            for row in  add_info_table:
                addi_info.append({
                    "key": row.query_selector("xpath=//th").inner_text().strip(),
                    "value": row.query_selector("xpath=//td").inner_text().strip()
            })
        except Exception:
            addi_info = None
        try:
            about_item = page2.query_selector("xpath=//ul[contains(@class, 'a-unordered-list a-vertical a-spacing-mini')]").inner_text()
        except Exception:
            about_item = None
        product_list.append({
            "title": title,
            "image_urls": image_urls,
            "shop_name": shop_name,
            "total_rating": total_rating,
            "emi": emi,
            "price": price,
            "star_rating": star_rating,
            "delivery": delivery,
            "date": date,
            "status": status,
            "add_protection_plan": add_protection_plan,
            "quantity": quantity,
            "offer": offer,
            "specification": specs,
            "additinal_information": addi_info,
            "about_item": about_item
        })
        browser.close()
        return product_list

    # >> Passed url of product for scrape reviews
    def scrape_reviews(self, product_url: str) -> None:
        """ This method to Scrape Product reviews

        Args:
            product_url (str): return list product urls
        """
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        url = "https://www.amazon.in"
        page = context.new_page()
        page.goto(url)
        time.sleep(3)
        page.locator("xpath=//div[contains(@id, 'nav-xshop')]//a[contains(text(), 'Mobiles')]").click()
        time.sleep(3)
        urls = page.query_selector_all("xpath=//a[contains(@class, 'a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal')]")

        review_details = []
        for url in urls:
            product_url = f"https://www.amazon.in{url.get_attribute('href')}"
            page2 = context.new_page()
            page2.goto(product_url)
            time.sleep(3)
            ratings = page2.query_selector_all("xpath=//td[contains(@class, 'aok-nowrap')]//span//a")
            if not ratings:
                page2.close()
                continue
            review_list = []
            start_rating = []
            for rating in ratings:
                rating_url = f"https://www.amazon.in{rating.get_attribute('href')}"
                page3 = context.new_page()
                page3.goto(rating_url)
                time.sleep(3)

                reviews = page3.query_selector_all("xpath=//div[contains(@class, 'a-section review aok-relative')]")
                for review in reviews:
                    profile_name = review.query_selector("xpath=//span[contains(@class, 'a-profile-name')]").inner_text()
                    try:
                        review_title = review.query_selector("xpath=//a[contains(@data-hook, 'review-title')]//span").inner_text()
                    except Exception as e:
                        print("Exception:::", str(e))
                    try:
                        review_date = review.query_selector("xpath=//span[contains(@data-hook, 'review-date')]").inner_text()
                    except Exception as e:
                        review_date = None
                    try:
                        text = review.query_selector("xpath=//div//a[contains(@data-hook, 'format-strip')]").inner_html().split("<i")
                        color = text[0]
                    except Exception as e:
                        color = None
                    try:
                        size = text[1].split("</i>")[1]
                    except Exception as e:
                        size = None
                    try:
                        style_name = text[2].split("</i>")[1]
                    except Exception as e:
                        style_name = None
                    try:
                        verify = review.query_selector("xpath=//span[contains(@data-hook ,'avp-badge')]").inner_text()
                    except Exception as e:
                        verify = None
                    try:
                        description = review.query_selector("xpath=//span[contains(@data-hook, 'review-body')]//span").inner_text()
                    except Exception as e:
                        description = None
                    try:
                        image = review.query_selector("xpath=//img[contains(@alt, 'Customer image')]").inner_text()
                    except Exception:
                        image = None
                    try:
                        helpful = review.query_selector("xpath=//span[contains(@data-hook, 'helpful-vote-statement')]").inner_text()
                    except Exception as e:
                        helpful = None
                    review_dict = {
                        "profile": profile_name,
                        "title": review_title,
                        "review_date": review_date,
                        "colour": color,
                        "size": size,
                        "style_name": style_name,
                        "verify": verify,
                        "description": description,
                        "image": image,
                        "helpful": helpful,
                    }
                    review_list.append(review_dict)
                page3.close()
                try:
                    rating_star = rating.inner_text()
                except:
                    rating_star = None
                start_rating.append({
                    "rating": rating_star,
                    "reviews":review_list
                })
            try:
                title = url.inner_text()
            except Exception:
                title = None
            review_details.append({
                "product": title,
                "rating": start_rating
            })
            page2.close()
        save_response(review_details, "reviews.json", "Data/amazon/")
        page.close()
        browser.close()

if __name__ == '__main__':
    """ Main Block """
    amazon = Amazon()

    with sync_playwright() as p:
        amazon.intro()
        # amazon.get_category()
        # amazon.get_asincode()
        json_path = os.path.join(os.path.dirname(__file__), "Data/amazon/")
        with open(os.path.join(json_path, "category_list.json"), "r", encoding="utf-8") as category:
            data = json.load(category)
        for i in data:
            for j in i:
                for k in j['sub_category']:
                    for l in k['product']:
                        try:
                            if l['details']:
                                continue
                        except Exception:
                            print("Exception:")
                        try:
                            l['details'] = amazon.get_product_details(l['asin_code'])
                        except Exception:
                            continue
                        save_response(data, "category_list2.json", "Data/amazon/")
        # >> Passed Url of the products
        amazon.scrape_reviews("https://www.amazon.in/s?rh=n%3A1389401031&fs=true&ref=lp_1389401031_sar")
