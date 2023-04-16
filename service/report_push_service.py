import json
import datetime
import requests

from common.api.common_result import R
from common.models.report_info import ReportInfo
from common.models.campus_info import CampusInfo
from common.utils.wxapi_util import WxApiUtil

from common.enums.report_status_enum import ReportStatus
from common.enums.report_types_enum import ReportTypes

class ReportPushService:
    qy_token = ""
    message_dict = {}

    @classmethod
    def update_token(self):
        self.qy_token = WxApiUtil.getQyAccessToken()
    
    @classmethod
    def getime(self):
        return int(datetime.datetime.now().timestamp())
    
    @classmethod
    def push(self, report_id): # 报障单推送函数
        """
        @param report_id: 需要推送的报障单的ID
        """
        self.update_token()
        
        report_info = ReportInfo.query.filter(id = report_id).first()
        
        campus_name = CampusInfo.query.filter(id = report_info.campus_id).first().name
        type_name = ReportTypes.get_type_name(report_info.type) + "报障"
        status_name = ReportStatus.MAP.value[report_info.status]
        report_info_dict = {
            '姓名' : report_info.name,
            '类型' : type_name,
            '电话' : report_info.phone,
            '地址' : report_info.address,
            '故障描述' : report_info.description,
            '状态' : status_name
        }
        
        report_info_str = ""
        for (key, value) in report_info_dict.items():
            report_info_str += key + "：" + value + "\n"
        report_info_str = report_info_str[:-1]
        print(report_info_str) # FIXME! debug
        
        from application import app
        
        WX_QY_PARTY = ""
        match campus_name:
            case '大学城校区':
                WX_QY_PARTY = app.config['WX_QY_PARTY_GZ']
            case '中山校区':
                WX_QY_PARTY = app.config['WX_QY_PARTY_ZS']
            case '云浮校区': # FIXME in profile_config.py
                WX_QY_PARTY = app.config['WX_QY_PARTY_YF']
            case '测试':
                WX_QY_PARTY = app.config['WX_QY_PARTY_TEST']
        
        json_report_dict = {
            "toparty" : WX_QY_PARTY,
            "agentid" : app.config['WX_QY_AGENT_ID'],
            "msgtype" : "text",
            "text" : {
                "content" : report_info_str
            },
            
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        
        json_report_str = json.dumps(json_report_dict)
        response_send = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(access_token = self.qy_token), data = json_report_str)
        
        res = json.loads(response_send.text)
        print(res)
        
        if res['errmsg'] != 'ok':
            print("report_push_server: push: response_send error!, errmsg = ")
            return False

        if report_info.status == ReportStatus.UNCONFIRMED:
            self.message_dict[report_id] = [self.getime(), res['msgid']]
        
        return True
    
    @classmethod
    def push(self, campus_name, report_id, message): # FIXME! 报障单推送函数(测试) 数据库搞定后删除
        """
        @param campus_name 报障单推送的校区
        @param report_id 报障单的ID
        @param message: 需要推送的报障单的信息
        """
        self.update_token()
        
        name = message[0]
        type_name = ReportTypes.get_type_name(message[1]) + "报障"
        phone = message[2]
        address = message[3]
        description = message[4]
        status = message[5]
        status_name = ReportStatus.MAP.value[status.value]
        
        report_info_dict = {
            '姓名' : name,
            '类型' : type_name,
            '电话' : phone,
            '地址' : address,
            '故障描述' : description,
            '状态' : status_name
        }
        
        report_info_str = ""
        for (key, value) in report_info_dict.items():
            report_info_str += key + "：" + value + "\n"
        report_info_str = report_info_str[:-1]
        print(report_info_str) # debug
        
        from application import app
        
        WX_QY_PARTY = ""
        match campus_name:
            case '大学城校区':
                WX_QY_PARTY = app.config['WX_QY_PARTY_GZ']
            case '中山校区':
                WX_QY_PARTY = app.config['WX_QY_PARTY_ZS']
            case '云浮校区': # FIXME in profile_config.py
                WX_QY_PARTY = app.config['WX_QY_PARTY_YF']
            case '测试':
                WX_QY_PARTY = app.config['WX_QY_PARTY_TEST']
        
        json_report_dict = {
            "toparty" : WX_QY_PARTY,
            "agentid" : app.config['WX_QY_AGENT_ID'],
            "msgtype" : "text",
            "text" : {
                "content" : report_info_str
            },
            
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        
        json_report_str = json.dumps(json_report_dict)
        response_send = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(access_token = self.qy_token), data = json_report_str)
        
        res = json.loads(response_send.text)
        print(res)
        
        if res['errmsg'] != 'ok':
            print("report_push_server: push: response_send error!, errmsg = ")
            return False

        if status == ReportStatus.UNCONFIRMED:
            self.message_dict[report_id] = [self.getime(), res['msgid']]
        
        return True
    
    @classmethod
    def recall(self, report_id): # 报障单撤回函数
        """
        @param report_id: 需要撤回的报障单的ID
        """
        self.update_token()
        
        json_recall_dict = {
            "msgid": ""
        }
        
        for (cur_report_id, cur_value) in self.message_dict.items():
            if self.getime() - cur_value[0] > 86400:
                del self.message_dict[cur_report_id]
                continue
            if report_id != cur_report_id:
                continue
            
            json_recall_dict['msgid'] = cur_value[1]
            json_recall_str = json.dumps(json_recall_dict)
            response_send = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/recall?access_token={access_token}".format(access_token = self.qy_token), data = json_recall_str)
            response_dict = json.loads(response_send.text)
            if response_dict['errmsg'] != 'ok':
                print('report_push_server: recall: response_send error！errmsg = ')
                print(response_dict)
            
            del self.message_dict[cur_report_id]
            break
            
        return # FIXME! 数据库搞定再删
        self.push(report_id)  # 推送报障单当前状态