"""初始化数据库并写入种子数据

用法：
    python scripts/init_db.py

说明：本脚本创建数据表并写入示例事项库数据（以通用/示范性质为主，
实际使用时由后台依据各区县真实政策维护更新）。
"""
import sys
from pathlib import Path

# 确保可导入 app 包
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import Base, engine
from app.models.entities import (
    Category, District, Matter, Material, Pitfall, ServiceWindow, Template,
)


def seed(db):
    # ---------- 分类 ----------
    categories = [
        ("hukou", "户籍", "hukou", "#4F7CFF", "户口迁移、落户、户籍证明等"),
        ("shebao", "社保医保", "shebao", "#2EB872", "参保登记、缴费、报销、转移接续"),
        ("gongjijin", "公积金", "gongjijin", "#F5A623", "公积金缴存、提取、贷款"),
        ("budongchan", "不动产", "budongchan", "#8B6FE8", "不动产登记、抵押、查询"),
        ("hunyin", "婚姻生育", "hunyin", "#FF6B9D", "婚姻登记、生育登记、生育津贴"),
        ("ruxue", "入学", "ruxue", "#36B9D9", "入学报名、学区、转学"),
        ("yanglao", "养老补贴", "yanglao", "#FF8C42", "养老金认证、高龄补贴、养老服务"),
        ("zhengjian", "证件办理", "zhengjian", "#5C6BC0", "身份证、居住证、护照等证件"),
    ]
    for code, name, icon, color, desc in categories:
        db.add(Category(code=code, name=name, icon=icon, color=color, description=desc))

    # ---------- 区县（示例） ----------
    districts = [
        ("110101", "东城区", "北京市", "北京市"),
        ("110105", "朝阳区", "北京市", "北京市"),
        ("110106", "丰台区", "北京市", "北京市"),
    ]
    for code, name, city, province in districts:
        db.add(District(code=code, name=name, city=city, province=province))

    db.flush()

    cat_map = {c.code: c.id for c in db.query(Category).all()}
    dis_map = {d.code: d.id for d in db.query(District).all()}

    # ---------- 事项：以身份证换领为例 ----------
    m = Matter(
        category_id=cat_map["zhengjian"],
        code="shenfenzheng_banli",
        name="居民身份证换领、补领",
        short_name="身份证换领",
        summary="身份证到期换领、丢失补领的办理材料与流程指南",
        description="居民身份证有效期满、损坏、丢失的，可向常住户口所在地或居住地公安机关申请换领、补领。本工具仅提供材料与流程指引，实际办理以窗口为准。",
        is_online=True,
        is_offline=True,
        fee_type="charged",
        fee_desc="到期换领工本费 20 元/证；损坏换领、丢失补领 40 元/证（具体以当地为准）。",
        time_limit="20 个工作日内（可自愿选择加急）",
        legal_basis="《中华人民共和国居民身份证法》",
        official_title="居民身份证申领登记办法（公安部）",
        official_url="https://www.gov.cn/",
        official_source="国家政务服务平台",
        need_appointment=True,
        appointment_note="部分城市需通过政务小程序提前预约，现场亦可取号排队。",
        is_high_frequency=True,
        elderly_tip="60 岁以上老人可在窗口优先办理，可致电就近派出所咨询上门服务。",
    )
    db.add(m)
    db.flush()

    materials = [
        Material(matter_id=m.id, name="居民户口簿", material_type="required", copy_requirement="原件", need_electronic=False, quantity=1, note="用于核对身份信息", sort_order=1),
        Material(matter_id=m.id, name="原居民身份证", material_type="required", copy_requirement="原件", need_electronic=False, quantity=1, note="换领时需交回原证", sort_order=2),
        Material(matter_id=m.id, name="申领登记表", material_type="required", copy_requirement="原件", need_electronic=False, quantity=1, note="窗口现场填写", sort_order=3),
        Material(matter_id=m.id, name="本人近期免冠照片", material_type="required", copy_requirement="电子版", need_electronic=True, quantity=1, note="各地要求不同，部分地区现场采集", sort_order=4),
        Material(matter_id=m.id, name="监护人身份证", material_type="optional", copy_requirement="原件", need_electronic=False, quantity=1, note="未满 16 周岁需提供", sort_order=5),
    ]
    for x in materials:
        db.add(x)

    pitfalls = [
        Pitfall(matter_id=m.id, title="照片规格不达标", content="身份证照片需白底、免冠、露双耳，不得佩戴首饰，部分地区对服装颜色有要求，建议现场采集。", tag="照片"),
        Pitfall(matter_id=m.id, title="未预约直接前往", content="高峰时段部分政务大厅要求预约，未预约可能无法取号，建议提前通过政务小程序确认。", tag="预约"),
        Pitfall(matter_id=m.id, title="户籍与居住地不一致", content="异地办理需满足当地居住登记要求，先确认是否支持异地换领。", tag="材料"),
    ]
    for x in pitfalls:
        db.add(x)

    windows = [
        ServiceWindow(
            matter_id=m.id, district_id=dis_map["110101"],
            name="东城区政务服务中心公安窗口", address="北京市东城区（示例地址）",
            office_time="周一至周五 9:00-17:00（法定节假日除外）",
            phone="010-12345", parking="周边停车场较少，建议绿色出行",
            bus="地铁 X 号线 X 站 A 口出，步行约 300 米",
            appointment_url="https://www.gov.cn/",
            queue_note="工作日早高峰取号排队约 30-60 分钟，建议错峰办理",
        ),
    ]
    for x in windows:
        db.add(x)

    # ---------- 事项：居住证办理 ----------
    m2 = Matter(
        category_id=cat_map["zhengjian"],
        code="juzhuzheng_banli",
        name="居住证申领",
        short_name="居住证办理",
        summary="在居住地连续居住并符合条件的，可申领居住证",
        description="在居住地居住并办理暂住登记满半年，且符合合法稳定就业、住所、连续就读条件之一的，可申领居住证。",
        is_online=True,
        is_offline=True,
        fee_type="free",
        fee_desc="首次申领免费",
        time_limit="15 个工作日内",
        legal_basis="《居住证暂行条例》",
        official_title="居住证暂行条例",
        official_url="https://www.gov.cn/",
        official_source="国家政务服务平台",
        need_appointment=False,
        appointment_note="可通过当地政务 APP 线上申请，线下领取",
        is_high_frequency=True,
        elderly_tip="不熟悉线上操作可到社区服务站由工作人员协助办理。",
    )
    db.add(m2)
    db.flush()

    for x in [
        Material(matter_id=m2.id, name="本人身份证", material_type="required", copy_requirement="原件+复印件", need_electronic=False, quantity=1, note="复印件含正反面", sort_order=1),
        Material(matter_id=m2.id, name="居住证明（租赁合同/房产证明/单位宿舍证明）", material_type="required", copy_requirement="原件+复印件", need_electronic=False, quantity=1, note="三选一", sort_order=2),
        Material(matter_id=m2.id, name="近期免冠照片", material_type="required", copy_requirement="电子版", need_electronic=True, quantity=1, note="白底 1 寸", sort_order=3),
        Material(matter_id=m2.id, name="就业/就读证明", material_type="optional", copy_requirement="原件", need_electronic=False, quantity=1, note="符合就业/就读条件时提供", sort_order=4),
    ]:
        db.add(x)

    for x in [
        Pitfall(matter_id=m2.id, title="居住登记未满半年", content="多数地区要求办理暂住登记满半年方可申领，提前查询当地起算时间。", tag="时间"),
        Pitfall(matter_id=m2.id, title="地址变更未更新", content="搬家后需及时更新居住登记地址，否则影响续签。", tag="材料"),
    ]:
        db.add(x)

    # ---------- 事项：社保参保登记 ----------
    m3 = Matter(
        category_id=cat_map["shebao"],
        code="shebao_canbao",
        name="灵活就业人员社保参保登记",
        short_name="灵活就业参保",
        summary="灵活就业人员参加养老、医疗保险的登记与缴费指引",
        description="无雇工的个体工商户、未在用人单位参保的非全日制从业人员等灵活就业人员，可自愿参加职工基本养老和医疗保险。",
        is_online=True,
        is_offline=False,
        fee_type="mixed",
        fee_desc="按当地缴费基数与比例按月缴纳，具体以社保部门公布为准",
        time_limit="即时办理，缴费按季度/年度",
        legal_basis="《中华人民共和国社会保险法》",
        official_title="社会保险法",
        official_url="https://www.gov.cn/",
        official_source="国家政务服务平台",
        need_appointment=False,
        appointment_note="支持线上办理，无需现场排队",
        is_high_frequency=True,
    )
    db.add(m3)
    db.flush()

    for x in [
        Material(matter_id=m3.id, name="本人身份证", material_type="required", copy_requirement="原件", need_electronic=False, quantity=1, note="线上需上传正反面", sort_order=1),
        Material(matter_id=m3.id, name="社保卡/银行卡", material_type="required", copy_requirement="原件", need_electronic=False, quantity=1, note="用于缴费绑定", sort_order=2),
        Material(matter_id=m3.id, name="灵活就业证明（如有）", material_type="optional", copy_requirement="原件", need_electronic=False, quantity=1, note="部分地区要求", sort_order=3),
    ]:
        db.add(x)

    for x in [
        Pitfall(matter_id=m3.id, title="缴费基数选择", content="缴费基数影响未来养老金，量力而行，可咨询当地 12333。", tag="费用"),
    ]:
        db.add(x)

    # ---------- 事项：高龄津贴 ----------
    m4 = Matter(
        category_id=cat_map["yanglao"],
        code="gaoling_buzhu",
        name="高龄津贴申领",
        short_name="高龄津贴",
        summary="年满 80 周岁以上老年人申领高龄津贴",
        description="各地对年满 80 周岁及以上的老年人发放高龄津贴，标准与年龄门槛因地区而异。",
        is_online=True,
        is_offline=True,
        fee_type="free",
        fee_desc="免费申领",
        time_limit="按季度或年度发放",
        legal_basis="各地高龄津贴办法",
        official_title="高龄津贴申领指南",
        official_url="https://www.gov.cn/",
        official_source="当地民政局",
        need_appointment=False,
        appointment_note="可由家属代办，社区可协助",
        is_high_frequency=True,
        elderly_tip="高龄津贴通常需主动申请，可由子女代办，社区网格员可上门协助。",
    )
    db.add(m4)
    db.flush()

    for x in [
        Material(matter_id=m4.id, name="本人身份证", material_type="required", copy_requirement="原件+复印件", need_electronic=False, quantity=1, note="含正反面", sort_order=1),
        Material(matter_id=m4.id, name="户口簿", material_type="required", copy_requirement="原件+复印件", need_electronic=False, quantity=1, note="首页及本人页", sort_order=2),
        Material(matter_id=m4.id, name="银行卡", material_type="required", copy_requirement="复印件", need_electronic=False, quantity=1, note="用于发放津贴", sort_order=3),
        Material(matter_id=m4.id, name="近期照片", material_type="optional", copy_requirement="电子版", need_electronic=True, quantity=1, note="部分地区要求", sort_order=4),
    ]:
        db.add(x)

    for x in [
        Pitfall(matter_id=m4.id, title="漏报年龄门槛", content="高龄津贴年龄门槛各地不同（80 或 90 岁），提前向社区确认。", tag="政策"),
    ]:
        db.add(x)

    db.commit()

    # ---------- 模板 ----------
    templates = [
        Template(
            code="shenqingshu", name="个人申请书（通用）", template_type="申请书",
            content="个人申请书\n\n致：____________（受理单位）\n\n本人______，身份证号____________，现因____________事项，特向贵单位提出申请。\n\n申请事项：____________\n申请理由：____________\n\n本人承诺所提交材料真实有效，如有虚假愿承担相应责任。\n\n此致\n敬礼\n\n申请人（签字）：____________\n联系电话：____________\n日期：____年____月____日",
            usage_note="适用于多种个人申请场景，可按需增删。",
        ),
        Template(
            code="qingkuangshuoming", name="情况说明", template_type="情况说明",
            content="情况说明\n\n致：____________（受理单位）\n\n本人______，身份证号____________，现就____________事项说明如下：\n\n一、基本情况：____________\n二、事由经过：____________\n三、补充说明：____________\n\n特此说明。\n\n说明人（签字）：____________\n日期：____年____月____日",
            usage_note="用于材料缺失或情况特殊时的书面说明。",
        ),
        Template(
            code="chengnuoshu", name="承诺书（材料真实性）", template_type="承诺书",
            content="承诺书\n\n本人______，身份证号____________，就办理____________事项，郑重承诺如下：\n\n一、本人所提供的全部材料真实、合法、有效；\n二、本人已知晓并遵守相关法律法规及办理要求；\n三、如材料存在虚假，本人愿承担由此产生的一切法律后果。\n\n承诺人（签字）：____________\n日期：____年____月____日",
            usage_note="用于承诺材料真实性等场景。",
        ),
    ]
    for t in templates:
        db.add(t)

    db.commit()
    print("✅ 种子数据写入完成")


def main():
    # 建表
    print("正在创建数据表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据表创建完成")

    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
