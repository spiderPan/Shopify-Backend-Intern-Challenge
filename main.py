import requests
from menulist import MenuList


DATAURL = 'https://backend-challenge-summer-2018.herokuapp.com/challenges.json'


def getData(url, param):
    # Read JSON from URL
    r = requests.get(url, params=param)
    return r.json()


def validateMenu(menus, menuList=[]):
    for menu in menus:
        id = menu.get('id')
        parentID = menu.get('parent_id', 0)
        childrenIDs = menu.get('child_ids', [])
        root_id = id if parentID == 0 else parentID
        m = MenuList(root_id)
        m.add_child(childrenIDs)
        mergeable_list = [menuitem for menuitem in menuList if menuitem.is_mergeable(m)]
        if len(mergeable_list) == 0:
            menuList.append(m)
        else:
            for menuitem in mergeable_list:
                menuitem = menuitem.merge_menulist(m)

    return menuList


def findNextURLParam(pagination):
    if pagination['current_page'] * pagination['per_page'] <= pagination['total']:
        return {'page': pagination['current_page'] + 1, 'id': 1}
    else:
        return False


def findInvalidateMenus(url, param={}, invalidateMenu=[]):
    data = getData(url, param)
    nextURLParam = findNextURLParam(data['pagination'])
    invalidateMenu = validateMenu(data['menus'], invalidateMenu)
    if nextURLParam:
        return findInvalidateMenus(url, nextURLParam, invalidateMenu)

    return invalidateMenu


def main():
    invalidatedMenu = []
    data = findInvalidateMenus(DATAURL, {}, invalidatedMenu)
    for item in data:
        print item.get_format()

main()
