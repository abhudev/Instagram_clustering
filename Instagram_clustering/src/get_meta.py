# Ger the metadata and store to a text file
# Text file is created via I/O redirection

from igramscraper.instagram import Instagram # pylint: disable=no-name-in-module

instagram = Instagram(sleep_between_requests=1.5)

medias = instagram.get_medias_by_tag('climatechange', count=50000)

for media in medias:
    print(media)
    print('Account info:')
    account = media.owner
    print('Id', account.identifier)
    # print('Username', account.username)
    # print('Full Name', account.full_name)
    # print('Profile Pic Url', account.get_profile_picture_url_hd())
    print('--------------------------------------------------')