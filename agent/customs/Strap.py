from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
from maa.context import Context

import time

from .utils import Tasker, parse_query_args, Prompt, RecoHelper, Judge, PresetLoader
from .Counter import counter_manager

index = 0


# 记录检查
@AgentServer.custom_action("init_strap_upgrade")
class InitStrapUpgrade(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index

        try:
            index = 0
            return True

        except Exception as e:
            return Prompt.error("初始化卡带升级", e)


# 选择下一个升级卡带
@AgentServer.custom_action("select_next_strap")
class SelectNextStrap(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index

        try:
            if index > 3:
                return False

            context.override_pipeline(
                {"卡带升级_切换卡带": {"target": [66, 442 + index * 75, 1, 1]}}
            )
            index += 1

            return True

        except Exception as e:
            return Prompt.error("切换卡带", e)


target_attr = set()
is_only_high = True


# 初始化卡带词条
@AgentServer.custom_action("set_strap_entry")
class SetStrapEntry(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global target_attr

        try:
            target_attr = set()
            return True
        except Exception as e:
            return Prompt.error("初始化卡带词条", e)


# 设置卡带属性
@AgentServer.custom_action("set_strap_attr")
class SetStrapAttr(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global target_attr

        try:
            args = parse_query_args(argv)
            attr = args.get("attr")

            if attr:
                target_attr.add(attr)
                Prompt.log(f"将选择卡带属性：{attr}")

            return True
        except Exception as e:
            return Prompt.error("设置卡带属性", e)


# 设置卡带属性值
@AgentServer.custom_action("set_strap_value")
class SetStrapValue(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global is_only_high

        try:
            args = parse_query_args(argv)
            level = args.get("level")

            is_only_high = level == "high"
            if is_only_high:
                Prompt.log("将仅选择较高值")

            return True
        except Exception as e:
            return Prompt.error("设置卡带属性值", e)


# 从 presets 加载卡带属性数据
strap_attrs = PresetLoader.read("strap_attr")
normal_attr = strap_attrs["normal_attr"]
special_attr1 = strap_attrs["special_attr1"]
special_attr2 = {
    "免疫力": ["4.5", "7.5"],
    "护甲": ["1.2", "1.2"],
    "坚韧": ["0.9", "1.5"],
    "凝神": ["9", "15"],
    "安定": ["9", "15"],
    "忍耐": ["3.6", "6"],
    "易愈": ["6", "10"],
    "坚壁": ["2.4", "4"],
    "护甲": ["1.2", "2"],
    "钝化": ["10", "15"],
    "散射化": ["10", "15"],
    "完璧": ["2.1", "3.5"],
    "逆境": ["6", "10"],
    "抗压": ["7.2", "12"],
    "护甲": ["1.2", "3"],
}


# 设置保底项
guaranteed = True


@AgentServer.custom_action("allow_strap_guaranteed")
class SetStrapValue(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global guaranteed

        try:
            args = parse_query_args(argv)
            value = args.get("value", "true")
            value = value.lower() == "true"

            guaranteed = value
            if guaranteed:
                Prompt.log("将使用较低值作为保底项")

            return True
        except Exception as e:
            return Prompt.error("设置卡带属性值", e)


# 设置目标项
@AgentServer.custom_action("set_strap_target")
class SetStrapTarget(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global target_attr
        try:
            rh = RecoHelper(context)
            for attr in target_attr:
                if "特殊词条" in attr:
                    special_list = (
                        special_attr1 if attr == "特殊词条1" else special_attr2
                    )
                    for special_attr in special_list:
                        if rh.recognize(
                            "卡带词条_识别目标属性", {"expected": f"^{special_attr}$"}
                        ).hit():
                            rh.click()
                            break
                else:
                    rh.recognize(
                        "卡带词条_识别目标属性", {"expected": f"^{attr}$"}
                    ).click()
                time.sleep(0.2)
            return True
        except Exception as e:
            return Prompt.error("设置卡带属性值", e)


# 检测属性词条
@AgentServer.custom_recognition("check_strap_attr")
class CheckStrapAttr(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        global target_attr, is_only_high, normal_attr, special_attr1, special_attr2, guaranteed

        try:
            # 识别
            results = (
                RecoHelper(context, argv)
                .recognize("卡带词条_识别区域")
                .reco_detail.all_results
            )
            text = ""
            for result in results:
                if result.text:
                    text += result.text
            if text == "":
                return RecoHelper.NoResult

            # 判断
            for attr in target_attr:
                # 特殊字段
                if "特殊词条" in attr:
                    special_list = (
                        special_attr1 if attr == "特殊词条1" else special_attr2
                    )
                    for special_attr in special_list:
                        # 非目标属性
                        if special_attr not in text:
                            continue
                        # 检测值
                        values = special_list[special_attr]
                        is_hit = Judge.exact_number(text, values[1])
                        if Judge.exact_number(text, values[0]):
                            if not is_only_high:
                                is_hit = True
                            if not is_hit and guaranteed:
                                RecoHelper(context, argv).recognize(
                                    "卡带词条_使用新特征"
                                ).click()
                            Prompt.log("使用较低值作为保底")
                            time.sleep(0.8)
                        # 命中时返回结果
                        if is_hit:
                            return RecoHelper.rt(results[0].box, text=text)
                # 通用字段
                else:
                    values = normal_attr.get(attr, None)
                    attr = attr.rstrip("%")
                    # 非目标属性
                    if attr not in text:
                        continue
                    # 检测值
                    is_hit = Judge.exact_number(text, values[1])
                    if Judge.exact_number(text, values[0]):
                        if not is_only_high:
                            is_hit = True
                        if not is_hit and guaranteed:
                            RecoHelper(context, argv).recognize(
                                "卡带词条_使用新特征"
                            ).click()
                            Prompt.log("使用较低值作为保底")
                            time.sleep(0.8)
                    # 命中时返回结果
                    if is_hit:
                        return RecoHelper.rt(results[0].box, text=text)

            return RecoHelper.NoResult
        except Exception as e:
            return Prompt.error("检测属性词条", e, reco_detail=True)


# 总结卡带消耗
@AgentServer.custom_action("summary_strap_value")
class SummaryStrapValue(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            is_hit = True if args.get("hit") == "true" else False

            count = counter_manager.get().get_count()
            if not is_hit:
                count -= 1
            Prompt.log(
                f"本次约消耗 {count*10*5} 个整流元件与 {count*0.5*5:.1f}w 数构银".replace(
                    ".0w", "w"
                )
            )
            return True
        except Exception as e:
            return Prompt.error("总结卡带消耗", e)
