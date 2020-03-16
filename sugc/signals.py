# @receiver(post_save, sender=FlyingList)
# def email_flying_list(sender, **kwargs):
#     members = sender.members
#     driver = sender.driver
#     # TODO: Make better email templates
#     driver.email_user('Flying %s'.format(sender.date), 'Driver')
#     for member in members:
#         member.email_user('Flying %s'.format(sender.date), 'Member. Driver is %s'.format(driver.name))
