emails_list = ['vasya@mail.ru',
          'akakiy@yandex.ru',
          'spyderman@yandex.ru',
          'XFiles@gmail.com',
          'hello@mail.ru',
          'noname@gmail.com',
          'DonaldTrump@mail.ru',
          'a768#af@yandex.ru',
          'Ivan_Ivanovich@yandex.ru',
          'thebestmail@yandex.ru']

# create list with not uniq domains
full_domain_list = []
for email in emails_list:
    curr_domain = email[email.find('@')+1:]
    full_domain_list.append(curr_domain)
print(full_domain_list)

# make list with uniq domains
uniq_domain_set = set(full_domain_list)
uniq_domain_list = list(uniq_domain_set)
print(uniq_domain_list)

# calc domain counts and create result dictionary
emails_dict = {}
for curr_domain in uniq_domain_list:
    curr_count = full_domain_list.count(curr_domain)
    emails_dict[curr_domain] = curr_count
print(emails_dict)




