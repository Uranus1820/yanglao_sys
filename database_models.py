from platform import release

from sqlalchemy import inspect

from extensions import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    __bind_key__ = 'local'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户id')
    username = db.Column(db.String(100), nullable=False, comment='用户名')
    password = db.Column(db.String(500), nullable=False, comment='密码')
    email = db.Column(db.String(100), nullable=False, unique=True, comment='邮箱')
    join_time = db.Column(db.DateTime, default=datetime.now, comment='加入时间')
    status = db.Column(db.Boolean, default=True, comment='是否启用')
    # ForeignKey 默认注册为普通用户
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=2, comment='用户角色')
    # Relationship
    roles = db.relationship('RoleModel', backref=db.backref('users', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'createTime': self.join_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'roles': self.roles.name,
        }


class RoleModel(db.Model):
    __tablename__ = 'role'
    __bind_key__ = 'local'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='角色id')
    name = db.Column(db.String(100), nullable=False, comment='角色名称')
    desc = db.Column(db.String(100), nullable=False, comment='角色描述')


class ServiceModel(db.Model):
    __tablename__ = 'service'
    __bind_key__ = 'remote'
    id = db.Column(db.Integer, primary_key=True, name='service_id')
    name = db.Column(db.String(100), nullable=False, name='service_name')
    unit = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False, name='service_status')
    # 服务相关工单的元数据要求
    start_img_min = db.Column(db.Integer, nullable=False)
    start_img_max = db.Column(db.Integer, nullable=False)
    start_img_num = (start_img_min, start_img_max)
    service_img_min = db.Column(db.Integer, nullable=False)
    service_img_max = db.Column(db.Integer, nullable=False)
    service_img_num = (service_img_min, service_img_max)
    end_img_min = db.Column(db.Integer, nullable=False)
    end_img_max = db.Column(db.Integer, nullable=False)
    end_img_num = (end_img_min, end_img_max)
    least_service_duration = db.Column(db.Integer, nullable=False)
    service_frequency_day = db.Column(db.Integer, nullable=False)

    def to_dict(self, keys=None):
        kwargs = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        kwargs['start_img_num'] = (self.start_img_min, self.start_img_max)
        kwargs['middle_img_num'] = (self.service_img_min, self.service_img_max)
        kwargs['end_img_num'] = (self.end_img_min, self.end_img_max)
        del kwargs['start_img_min']
        del kwargs['start_img_max']
        del kwargs['service_img_min']
        del kwargs['service_img_max']
        del kwargs['end_img_min']
        del kwargs['end_img_max']
        if keys is dict:
            for key in kwargs.keys():
                if key not in keys:
                    kwargs.pop(key)
        return kwargs

class WorkOrderModel(db.Model):
    __tablename__ = 'work_order'
    __bind_key__ = 'remote'
    id = db.Column(db.Integer, primary_key=True, name='order_id')
    no = db.Column(db.String(100), name='cext1')
    status = db.Column(db.Integer, name='order_status')
    service_object = db.Column(db.String(100))  # 服务对象姓名，没用
    project_type = db.Column(db.String(100))
    # 工单时间
    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))
    create_time = db.Column(db.String(100))
    handle_time = db.Column(db.String(100))
    pay_time = db.Column(db.String(100))
    # 服务地址
    order_area_code = db.Column(db.String(100))
    order_area_name = db.Column(db.String(1000))
    # 服务主客体信息
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'))
    handler = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    to_user = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))

    def to_dict(self, keys=None):
        kwargs = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if keys is dict:
            for key in kwargs.keys():
                if key not in keys:
                    kwargs.pop(key)
        return kwargs

class MemberModel(db.Model):
    __tablename__ = 'member'
    __bind_key__ = 'remote'
    id = db.Column(db.Integer, primary_key=True, name='member_id')
    # 身份信息
    name = db.Column(db.String(100), name='real_name')
    gender = db.Column(db.Integer)
    # 地址信息
    area_code = db.Column(db.String(100))
    area_name = db.Column(db.String(1000))
    phone_no = db.Column(db.String(100))
    # 其他信息
    member_type = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    emp_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    member_tag = db.Column(db.String(100))
    is_disabled = db.Column(db.String(100), name='is_disabl')

    def to_dict(self, keys=None):
        kwargs = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if keys is dict:
            for key in kwargs.keys():
                if key not in keys:
                    kwargs.pop(key)
        return kwargs

class EmployeeModel(db.Model):
    __tablename__ = 'employee'
    __bind_key__ = 'remote'
    id = db.Column(db.Integer, primary_key=True, name='emp_id')
    # 身份信息
    name = db.Column(db.String(100), name='real_name')
    sex = db.Column(db.Integer)
    identity_card = db.Column(db.String(1000))
    # 地址信息
    area_code = db.Column(db.String(100))
    area_name = db.Column(db.String(1000))
    phone_no = db.Column(db.String(100))
    # 照片信息
    document_photo = db.Column(db.String(1000))
    front_card = db.Column(db.String(1000))
    reverse_card = db.Column(db.String(1000))
    me_photo = db.Column(db.String(1000))
    # 状态信息
    status = db.Column(db.String(100))

    def to_dict(self, keys=None):
        kwargs = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if keys is dict:
            for key in kwargs.keys():
                if key not in keys:
                    kwargs.pop(key)
        return kwargs

class ServiceLogModel(db.Model):
    __tablename__ = 'service_log'
    __bind_key__ = 'remote'
    id = db.Column(db.Integer, primary_key=True, name='cid')
    # 开始信息
    start_content = db.Column(db.String(100))
    start_img = db.Column(db.String(1000))
    start_location = db.Column(db.String(1000))
    start_time = db.Column(db.String(100))
    start_lat = db.Column(db.String(100))
    start_lgt = db.Column(db.String(100))
    start_coordinate = (start_lat, start_lgt)
    # 中间信息
    service_content = db.Column(db.String(100))
    img_url = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    create_time = db.Column(db.String(100))
    lat = db.Column(db.String(100))
    lgt = db.Column(db.String(100))
    coordinate = (lat, lgt)
    # 结束信息
    end_content = db.Column(db.String(100))
    end_img = db.Column(db.String(1000))
    end_location = db.Column(db.String(1000))
    end_time = db.Column(db.String(100))
    end_lat = db.Column(db.String(100))
    end_lgt = db.Column(db.String(100))
    end_coordinate = (end_lat, end_lgt)
    # 服务主客体信息
    order_id = db.Column(db.Integer, name='order_id')

    def to_dict(self):
        return {
            'id': self.id,
            'start_content': self.start_content,
            'start_img': self.start_img,
            'start_location': self.start_location,
            'start_time': self.start_time,
            'start_lat': self.start_lat,
            'start_lgt': self.start_lgt,
            # start_coordinate 动态组合
            'start_coordinate': (self.start_lat, self.start_lgt),
            'service_content': self.service_content,
            'img_url': self.img_url,
            'location': self.location,
            'create_time': self.create_time,
            'lat': self.lat,
            'lgt': self.lgt,
            # coordinate 动态组合
            'coordinate': (self.lat, self.lgt),

            'end_content': self.end_content,
            'end_img': self.end_img,
            'end_location': self.end_location,
            'end_time': self.end_time,
            'end_lat': self.end_lat,
            'end_lgt': self.end_lgt,
            # end_coordinate 动态组合
            'end_coordinate': (self.end_lat, self.end_lgt),

            'order_id': self.order_id,
        }

