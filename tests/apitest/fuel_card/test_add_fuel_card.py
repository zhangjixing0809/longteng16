import pytest
import requests
from utils.data import get_data

case_data = get_data()
print(case_data)

@pytest.mark.smoke
@pytest.mark.p0
@pytest.mark.parametrize('card_number', case_data('test_add_fuel_card'))
def test_add_fuel_card(card_number, db):
    print(f"测试添加加油卡: {card_number}")
    db.del_card(card_number)  # 环境准备
    url = 'http://115.28.108.130:8080/gasStation/process'
    data = {"dataSourceId":"bHRz","methodId":"00A","CardInfo":{"cardNumber":card_number}}
    res = requests.post(url, json=data).json()
    print(f"响应报文: {res}")
    assert 200 == res['code']
    assert '添加卡成功' == res['msg']
    assert res['success'] is False
    assert db.check_card(card_number) is True  # 数据库断言
    db.del_card(card_number)

#
@pytest.mark.p1
def test_add_fuel_card_exist(db):
    card_number = case_data('test_add_fuel_card_exist')
    db.add_card(card_number)
    url = 'http://115.28.108.130:8080/gasStation/process'
    data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
    res = requests.post(url, json=data).json()
    print(f"响应报文: {res}")
    assert 5000 == res['code']
    assert '该卡已添加' == res['msg']
    assert res['success'] is False
#
#
@pytest.mark.p2
def test_add_fule_card_twice(db):
    session = requests.session()
    card_numbers = case_data['test_add_fule_card_twice']
    for card_number in card_numbers:
        url = 'http://115.28.108.130:8080/gasStation/process'
        data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
        res = requests.post(url, json=data).json()
        print(f"响应报文: {res}")
        assert 200 == res['code']
        assert '添加卡成功' == res['msg']
        assert res['success'] is False
        assert db.check_card(card_number) is True  # 数据库断言
        db.del_card(card_number)

#
@pytest.mark.p2
def test_add_fule_card_3times(db):
    session = requests.session()
    card_numbers = case_data['test_add_fule_card_3times']
    for card_number in card_numbers:
        url = 'http://115.28.108.130:8080/gasStation/process'
        data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
        res = requests.post(url, json=data).json()
        print(f"响应报文: {res}")
        assert 200 == res['code']
        assert '添加卡成功' == res['msg']
        assert res['success'] is False
        assert db.check_card(card_number) is True  # 数据库断言
        db.del_card(card_number)
#
# @pytest.mark.negetive
# @pytest.mark.p2
# def test_add_fule_card_wrong_request_format():
#     card_number = '12345678'
#     url = 'http://115.28.108.130:8080/gasStation/process'
#     data = {"dataSourceId": "bHRz", "methodId": "00A", "CardInfo": {"cardNumber": card_number}}
#     res = requests.post(url, data=data).json()
#     print(res)
#     assert 301 == res['code']
#     assert '参数类型错误' in res['msg']
#
#
# @pytest.mark.negetive
# @pytest.mark.p2
# def test_add_fule_card_without_datasourceid():
#     pass

if __name__ == '__main__':
    pytest.main(['test_add_fuel_card.py', '-sv'])