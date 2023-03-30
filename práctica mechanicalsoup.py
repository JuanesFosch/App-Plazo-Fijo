import mechanicalsoup

browser= mechanicalsoup.StatefulBrowser()

browser.open("http://httpbin.org/")


browser.follow_link("forms")
browser.url
browser.page

browser.page.find_all('legend')

browser.select_form('form[action="/post"]')

browser.form.print_summary()

browser["custname"]='Juan'
browser["custtel"]='261'
browser["custemail"]= "juan@mail.com"
browser["comments"]="Pizza"
browser["size"]="medium"
browser["topping"]=("mushroom","onion")


browser.form.print_summary()

response = browser.submit_selected()

print(response)

