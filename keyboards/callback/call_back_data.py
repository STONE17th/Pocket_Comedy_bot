from aiogram.utils.callback_data import CallbackData

menu_main = CallbackData('main', 'menu', 'button')
menu_search = CallbackData('search', 'menu', 'button')
event_navigation = CallbackData('EventNavigation', 'menu', 'list_target', 'list_id')
select_event = CallbackData('SelectEvent', 'menu', 'location', 'city',
                            'org_id', 'date', 'current_id')

