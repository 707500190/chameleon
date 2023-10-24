def add_module(parent_module_name, module_name, url):
    '''
    更新  原有基础添加 url
    :param parent_module_name: 现有父级模块
    :param module_name: 新增模块名称
    :param url: module默认url
    :return: dml sql
    '''
    arr_sql = {}
    parent_id_sql = f"select @pmId:=id from module where module_name = '{parent_module_name}'; "
    max_rank_sql = f"select @max_rank:= max(rank) from module where parent_id = @pmId;"

    insert_module_sql = f"INSERT INTO `module` (`module_name`, `parent_id`, `rank`, `module_url`, `module`, `create_at`, `update_at`, `tenant_id`, `is_platform`, `prefix`, `is_view`)" \
                        f"VALUES ('{module_name}', @pmId, @max_rank + 1, '{url}', '{url}', now(), NULL, NULL, 0, NULL, '0');"
    arr_sql["parent_id_sql"] = parent_id_sql
    arr_sql["max_rank_sql"] = max_rank_sql
    arr_sql["insert_module_sql"] = insert_module_sql
    return arr_sql


def but_exists_add_url(module_name, but_number, new_but_url):
    '''更新  原有基础添加 url'''
    arr_sql = {}
    module_sql = f"select @mId:=id from module where module_name = '{module_name}';"
    old_module_but_sql = f"select @bId:=id, @url := module_url from module_but where module_id = @mId and but_number = '{but_number}';"

    update_but_sql = f"update module_but SET module_url = (CONCAT(@url,',', '{new_but_url}')) where id = @bId;"
    arr_sql["module_sql"] = module_sql
    arr_sql["module_but_sql"] = old_module_but_sql
    arr_sql["update_but_sql"] = update_but_sql
    return arr_sql


def module_exists_add_but(module_name, but_url, but_code, but_name):
    arr_sql = {}
    '''module下面加按钮'''
    module_sql = f"select @mid := id from module where module_name = '{module_name}';"
    # module_id = mysql.execute_query(module_sql)
    arr_sql["module_sql"] = module_sql
    insert_but_sql = f"INSERT INTO `module_but` ( `but_name`, `but_number`, `module_url`, `create_at`, `update_at`, `module_id`, `is_view`)" \
                     f"VALUES ('{but_name}', '{but_code}', '{but_url}', now(), now(), @mid, '0');"
    arr_sql["but_sql"] = insert_but_sql
    return arr_sql


if __name__ == '__main__':
    # sql = but_exists_add_url("考核评价", "提交", "/xx/ras")
    sql = add_module("考核评价", "提ss交", "/xx/ras")
    print(sql)
