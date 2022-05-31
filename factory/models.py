from django.db import models
from django_currentuser.db.models import CurrentUserField


# Create your models here.
class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def inactives(self):
        return super().get_queryset().filter(is_active=False)


class BaseModel(models.Model):
    objects = BaseManager()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name="作成者", editable=False, null=True, blank=True,
    )
    last_updated_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_last_updated_by",
        verbose_name="最終更新者", editable=False, null=True, blank=True, on_update=True
    )
    is_active = models.BooleanField(default=True, verbose_name="有効")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class Maker(BaseModel):
    class Meta:
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー"

    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255, unique=True)


class MachineType(BaseModel):
    class Meta:
        verbose_name = "機械種別"
        verbose_name_plural = "機械種別"
        
    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255, unique=True)


class Machine(BaseModel):
    class Meta:
        verbose_name = "機械"
        verbose_name_plural = "機械"

    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255)
    maker = models.ForeignKey(
        Maker, verbose_name='メーカー', on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    machine_type = models.ForeignKey(
        MachineType, verbose_name='機械種別', on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    # factory = models.ForeignKey(
    #     Factory, verbose_name="保有工場", on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    detail = models.TextField("備考・詳細", blank=True, null=True)
    '''
    Spec Fields
    - name rule: spec_[large_category]_[middle_category]_[small_category]
    '''
    # capacity
    spec_capacity_each_axis_movement_amount_x = models.IntegerField('容量 / 各軸移動量[mm] / X', blank=True, null=True)
    spec_capacity_each_axis_movement_amount_y = models.IntegerField('容量 / 各軸移動量[mm] / Y', blank=True, null=True)
    spec_capacity_each_axis_movement_amount_z = models.IntegerField('容量 / 各軸移動量[mm] / Z', blank=True, null=True)
    spec_capacity_each_axis_movement_amount_w = models.IntegerField('容量 / 各軸移動量[mm] / W', blank=True, null=True)
    spec_capacity_others_effective_width = models.IntegerField('容量 / その他 / 有効門幅[mm]', blank=True, null=True)
    spec_capacity_others_effective_height = models.IntegerField('容量 / その他 / 有効門高さ[mm]', blank=True, null=True)
    spec_capacity_others_distance_from_table_top_to_spindle_end = models.CharField('容量 / その他 / テーブル上面から主軸端面までの距離[mm]', blank=True, null=True, max_length=255)
    spec_capacity_others_distance_from_column_front_to_main_axis = models.CharField('容量 / その他 / コラム前面から主軸中心までの距離[mm]', blank=True, null=True, max_length=255)
    spec_capacity_others_distance_from_pallet_top_to_main_axis = models.CharField('容量 / その他 / パレット上面から主軸中心までの距離[mm]', blank=True, null=True, max_length=255)
    spec_capacity_others_distance_from_spindle_end_from_pallet_top = models.CharField('容量 / その他 / パレット上面から主軸端面[mm]', blank=True, null=True, max_length=255)
    spec_capacity_others_distance_from_pallet_center_to_spindle_end = models.CharField('容量 / その他 / パレット中心線から主軸端面までの距離[mm]', blank=True, null=True, max_length=255)
    # table
    spec_table_table_dimension_vertical = models.IntegerField('テーブル/テーブル寸法[mm]/縦', blank=True, null=True)
    spec_table_table_dimension_beside = models.IntegerField('テーブル/テーブル寸法[mm]/横', blank=True, null=True)
    spec_table_others_table_maximum_loading_amount = models.IntegerField('テーブル/その他/テーブル最大積載量[kg]', blank=True, null=True)
    spec_table_work_surface_size_vertical = models.IntegerField('テーブル/作業面の大きさ[mm]/縦', blank=True, null=True)
    spec_table_work_surface_size_beside = models.IntegerField('テーブル/作業面の大きさ[mm]/横', blank=True, null=True)
    spec_table_work_surface_shape_t_groove_mark_dimension = models.IntegerField('テーブル/作業面の形状/T溝呼び寸法', blank=True, null=True)
    spec_table_work_surface_shape_width = models.IntegerField('テーブル/作業面の形状/幅[mm]', blank=True, null=True)
    spec_table_work_surface_shape_interval = models.IntegerField('テーブル/作業面の形状/間隔[mm]', blank=True, null=True)
    spec_table_work_surface_shape_number = models.IntegerField('テーブル/作業面の形状/本数', blank=True, null=True)
    spec_table_work_surface_shape_height = models.IntegerField('テーブル/作業面の形状/高さ[mm]', blank=True, null=True)
    spec_table_others_bevel_from_floor_to_table_work_surface = models.IntegerField('テーブル/その他/床面からテーブル作業面までの高さ[mm]', blank=True, null=True)
    spec_table_maximum_travel_distance_left_and_right = models.IntegerField('テーブル/最大移動距離[mm]/左右', blank=True, null=True)
    spec_table_maximum_travel_distance_front_and_back = models.IntegerField('テーブル/最大移動距離[mm]/前後', blank=True, null=True)
    spec_table_maximum_travel_distance_up_and_down = models.IntegerField('テーブル/最大移動距離[mm]/上下', blank=True, null=True)
    spec_table_maximum_work_dimension_vertical = models.IntegerField('テーブル/最大ワーク寸法[mm]/縦', blank=True, null=True)
    spec_table_maximum_work_dimension_beside = models.IntegerField('テーブル/最大ワーク寸法[mm]/横', blank=True, null=True)
    spec_table_maximum_work_dimension_height = models.IntegerField('テーブル/最大ワーク寸法[mm]/高さ', blank=True, null=True)
    spec_table_left_and_right_feed_speed_50_hz = models.IntegerField('テーブル/左右送り速度[mm/min]/50Hz', blank=True, null=True)
    spec_table_left_and_right_feed_speed_60_hz = models.IntegerField('テーブル/左右送り速度[mm/min]/60Hz', blank=True, null=True)
    spec_table_left_and_right_fast_forward_speed_50_hz = models.IntegerField('テーブル/左右早送り速度[mm/min]/50Hz', blank=True, null=True)
    spec_table_left_and_right_fast_forward_speed_60_hz = models.IntegerField('テーブル/左右早送り速度[mm/min]/60Hz', blank=True, null=True)
    spec_table_upper_and_lower_fast_feed_speed_50_hz = models.IntegerField('テーブル/上下早送り速度[mm/min]/50Hz', blank=True, null=True)
    spec_table_upper_and_lower_fast_feed_speed_60_hz = models.IntegerField('テーブル/上下早送り速度[mm/min]/60Hz', blank=True, null=True)
    spec_table_subtable_dimensions_vertical = models.IntegerField('テーブル/サブテーブル寸法/縦[mm]', blank=True, null=True)
    spec_table_subtable_dimensions_horizontal = models.IntegerField('テーブル/サブテーブル寸法/横[mm]', blank=True, null=True)
    # Pallet
    spec_palette_work_surface_size_vertical = models.IntegerField('パレット/作業面の大きさ/縦[mm]', blank=True, null=True)
    spec_palette_work_surface_size_horizontal = models.IntegerField('パレット/作業面の大きさ/横[mm]', blank=True, null=True)
    spec_palette_others_maximum_load_mass = models.IntegerField('パレット/その他/最大積載質量[kg]', blank=True, null=True)
    spec_palette_others_index_angle = models.IntegerField('パレット/その他/割り出し角度[°]', blank=True, null=True)
    spec_palette_others_maximum_loading_work_dimension = models.CharField('パレット/その他/最大積載ワーク寸法[mm]', blank=True, null=True, max_length=255)
    # 主軸
    spec_spindle_others_spindle_rotational_speed = models.CharField('主軸/その他/主軸回転速度[min^-1]', blank=True, null=True, max_length=255)
    spec_spindle_others_rotational_speed_range_transform_number = models.CharField('主軸/その他/回転速度域変換数', blank=True, null=True, max_length=255)
    spec_spindle_others_spindle_taper = models.CharField('主軸/その他/主軸テーパ', blank=True, null=True, max_length=255)
    spec_spindle_others_bearing_internal_diameter = models.CharField('主軸/その他/軸受内径[mm]', blank=True, null=True, max_length=255)
    spec_spindle_others_spindle_end_nose_shape = models.CharField('主軸/その他/主軸端ノーズ形状', blank=True, null=True, max_length=255)
    spec_spindle_others_spindle_through_hole_diameter = models.IntegerField('主軸/その他/主軸貫通穴径', blank=True, null=True)
    spec_spindle_others_spool_diameter = models.IntegerField('主軸/その他/主軸径', blank=True, null=True)
    spec_spindle_others_maximum_torque = models.CharField('主軸/その他/最大トルク[N・m]', blank=True, null=True, max_length=255)
    spec_spindle_others_base_rotation_speed = models.IntegerField('主軸/その他/基底回転数[min^-1]', blank=True, null=True)
    spec_spindle_others_spindle_air_blowing_device = models.BooleanField('主軸/その他/主軸エアブロー装置', default=False)
    # 主軸
    spec_spindle_others_spindle_quota_stop_device = models.BooleanField('主軸/その他/主軸定位置停止装置', default=False)
    # 送り速度
    spec_sending_speed_fast_forward_speed_x = models.IntegerField('送り速度/早送り速度[m/min]/X', blank=True, null=True)
    spec_sending_speed_fast_forward_speed_y = models.IntegerField('送り速度/早送り速度[m/min]/Y', blank=True, null=True)
    spec_sending_speed_fast_forward_speed_z = models.IntegerField('送り速度/早送り速度[m/min]/Z', blank=True, null=True)
    spec_sending_speed_fast_forward_speed_yl = models.IntegerField('送り速度/早送り速度[m/min]/YL', blank=True, null=True)
    spec_sending_speed_others_cutting_feed_rate = models.CharField('送り速度/その他/切削送り速度[mm/min]', blank=True, null=True, max_length=255)
    spec_sending_speed_others_jog_feed_rate = models.CharField('送り速度/その他/ジョグ送り速度[mm/min]', blank=True, null=True, max_length=255)
    spec_sending_speed_others_average_continuous_cutting_feed_rate = models.CharField('送り速度/その他/平均連続切削送り速度(X,Y,Z)[mm/min]', blank=True, null=True, max_length=255)
    spec_sending_speed_others_w_axis_feed_rate = models.CharField('送り速度/その他/W軸送り速度[mm/min]', blank=True, null=True, max_length=255)
    spec_sending_speed_others_manual_feed_rate = models.CharField('送り速度/その他/手動送り速度[mm/min]', blank=True, null=True, max_length=255)
    # ATC
    spec_atc_others_tool_shank_call_number = models.CharField('自動工具交換装置(ATC)/その他/ツールシャンク(呼び番号)', blank=True, null=True, max_length=255)
    spec_atc_others_pullstad_call_number = models.CharField('自動工具交換装置(ATC)/その他/プルスタッド(呼び番号)', blank=True, null=True, max_length=255)
    spec_atc_others_tool_storage_number = models.IntegerField('自動工具交換装置(ATC)/その他/工具収納本数', blank=True, null=True)
    spec_atc_others_tool_maximum_diameter_with_adjacent = models.CharField('自動工具交換装置(ATC)/その他/工具最大径(隣接工具あり)[mm]', blank=True, null=True, max_length=255)
    spec_atc_others_tool_maximum_diameter_without_adjacent = models.CharField('自動工具交換装置(ATC)/その他/工具最大径(隣接工具なし)[mm]', blank=True, null=True, max_length=255)
    spec_atc_others_tool_maximum_length = models.IntegerField('自動工具交換装置(ATC)/その他/工具最大長さ(ゲージラインより)[mm]', blank=True, null=True)
    spec_atc_others_tool_maximum_mass = models.IntegerField('自動工具交換装置(ATC)/その他/工具最大質量(モーメント)[kg(N・m)]', blank=True, null=True)
    spec_atc_others_tool_selection_method = models.CharField('自動工具交換装置(ATC)/その他/工具選択方式', blank=True, null=True, max_length=255)
    spec_atc_others_tool_replacement_time_tool_to_tool = models.CharField('自動工具交換装置(ATC)/その他/工具交換時間　ツール・ツー・ツール[s]', blank=True, null=True, max_length=255)
    spec_atc_others_tool_replacement_time_cut2cut = models.FloatField('自動工具交換装置(ATC)/その他/工具交換時間　カット・ツー・カット[s]', blank=True, null=True)
    spec_atc_others_tool_replacement_method = models.CharField('自動工具交換装置(ATC)/その他/工具交換方式', blank=True, null=True, max_length=255)
    spec_atc_others_magazine_turning_drive_motor = models.IntegerField('自動工具交換装置(ATC)/その他/マガジン旋回駆動用モータ[W]', blank=True, null=True)
    spec_atc_others_atc_arm_driving_motor = models.IntegerField('自動工具交換装置(ATC)/その他/ATCアーム駆動用モータ[W]', blank=True, null=True)   
    # 刃物台
    spec_knife_stand_others_claotorial_format = models.CharField('刃物台/その他/刃物台の形式', blank=True, null=True, max_length=255)
    spec_knife_stand_others_tool_mounting_number_of_tool_mounting = models.CharField('刃物台/その他/刃物台の工具取付本数[本]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_outer_diameter_byte_shank_dimension = models.IntegerField('刃物台/その他/外径バイトシャンク寸法[mm]', blank=True, null=True)
    spec_knife_stand_others_inner_diameter_tool_shank_diameter = models.IntegerField('刃物台/その他/内径工具シャンク径[mm]', blank=True, null=True)
    spec_knife_stand_others_blade_stand_indexing_time = models.IntegerField('刃物台/その他/刃物台割出し時間[sec/インデックス]', blank=True, null=True)
    spec_knife_stand_others_pressure_capacity = models.IntegerField('刃物台/その他/加圧能力[tf]', blank=True, null=True)
    spec_knife_stand_others_pressurable_ability = models.IntegerField('刃物台/その他/加圧能力[kN]', blank=True, null=True)
    spec_knife_stand_others_ability_occurrence_position = models.FloatField('刃物台/その他/能力発生位置(下死点上)[mm]', blank=True, null=True)
    spec_knife_stand_others_stroke_length = models.FloatField('刃物台/その他/ストローク長さ[mm]', blank=True, null=True)
    spec_knife_stand_number_of_strokes_fixed = models.IntegerField('刃物台/ストローク数[min^-1]/固定', blank=True, null=True)
    spec_knife_stand_number_of_strokes_variable = models.CharField('刃物台/ストローク数[min^-1]/可変', blank=True, null=True, max_length=255)
    spec_knife_stand_others_intermittent_num_of_strokes_per_min = models.IntegerField('刃物台/その他/許容断続毎分ストローク数[min^-1', blank=True, null=True)
    spec_knife_stand_others_die_height = models.IntegerField('刃物台/その他/ダイハイト[mm]', blank=True, null=True)
    spec_knife_stand_others_slide_adjustment_length = models.IntegerField('刃物台/その他/スライド調整長さ[mm]', blank=True, null=True)
    spec_knife_stand_slide_dimension_left_and_right = models.IntegerField('刃物台/スライド寸法[mm]/左右', blank=True, null=True)
    spec_knife_stand_slide_dimension_front_and_back = models.IntegerField('刃物台/スライド寸法[mm]/前後', blank=True, null=True)
    spec_knife_stand_bolster_dimensions_left_and_right = models.IntegerField('刃物台/ボルスター寸法[mm]/左右', blank=True, null=True)
    spec_knife_stand_bolster_dimensions_front_and_back = models.IntegerField('刃物台/ボルスター寸法[mm]/前後', blank=True, null=True)
    spec_knife_stand_others_thickness = models.IntegerField('刃物台/その他/厚さ', blank=True, null=True)
    spec_knife_stand_others_frame_gap = models.IntegerField('刃物台/その他/フレームギャップ[mm]', blank=True, null=True)
    spec_knife_stand_others_frame_inner_dimension = models.IntegerField('刃物台/その他/フレーム内側寸法[mm]', blank=True, null=True)
    spec_knife_stand_others_total_height = models.IntegerField('刃物台/その他/総高さ[mm]', blank=True, null=True)
    spec_knife_stand_basic_bolt_position_left_and_right = models.IntegerField('刃物台/基礎ボルト位置[mm]/左右', blank=True, null=True)
    spec_knife_stand_basic_bolt_position_front_and_back = models.IntegerField('刃物台/基礎ボルト位置[mm]/前後', blank=True, null=True)
    spec_knife_stand_hemed_area_left_and_right = models.IntegerField('刃物台/裾付面積[mm]/左右', blank=True, null=True)
    spec_knife_stand_hemed_area_front_and_back = models.IntegerField('刃物台/裾付面積[mm]/前後', blank=True, null=True)
    spec_knife_stand_maximum_dimensions_left_and_right = models.IntegerField('刃物台/最大寸法[mm]/左右', blank=True, null=True)
    spec_knife_stand_maximum_dimensions_front_and_back = models.IntegerField('刃物台/最大寸法[mm]/前後', blank=True, null=True)
    spec_knife_stand_others_main_electric_machine = models.CharField('刃物台/その他/主電動機[kW×P]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_air_pressure_used = models.CharField('刃物台/その他/使用空気圧力[kgf/cm^2]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_bending_length = models.FloatField('刃物台/その他/曲げ長さ[mm]', blank=True, null=True)
    spec_knife_stand_others_back_gauge_length = models.IntegerField('刃物台/その他/バックゲージ測長[mm]', blank=True, null=True)
    spec_knife_stand_others_down_speed = models.CharField('刃物台/その他/下降速度[mm/sec.]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_folding_speed = models.CharField('刃物台/その他/折り曲げ速度[mm/sec.]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_rising_speed = models.CharField('刃物台/その他/上昇速度[mm/sec.]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_main_motor = models.CharField('刃物台/その他/メインモーター[kW]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_motor_for_back_gauge = models.CharField('刃物台/その他/バックゲージ用モーター[W]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_number_of_control_axes = models.CharField('刃物台/その他/制御軸数', blank=True, null=True, max_length=255)
    spec_knife_stand_others_number_of_processes = models.CharField('刃物台/その他/工程数', blank=True, null=True, max_length=255)
    spec_knife_stand_others_display = models.CharField('刃物台/その他/表示[inch]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_machine_weight = models.FloatField('刃物台/その他/機械重量[ton]', blank=True, null=True)
    spec_knife_stand_others_gap_depth = models.IntegerField('刃物台/その他/ギャップ深さ[mm]', blank=True, null=True)
    spec_knife_stand_others_open_height = models.IntegerField('刃物台/その他/オープンハイト[mm]', blank=True, null=True)
    spec_knife_stand_others_number_of_cylinders = models.IntegerField('刃物台/その他/シリンダ数', blank=True, null=True)
    spec_knife_stand_others_tank_capacity = models.IntegerField('刃物台/その他/タンク容量[L]', blank=True, null=True)
    spec_knife_stand_others_quenching_speed = models.IntegerField('刃物台/その他/急閉じ速度[mm/s]', blank=True, null=True)
    spec_knife_stand_others_opening_speed = models.IntegerField('刃物台/その他/開き速度[mm/s]', blank=True, null=True)
    spec_knife_stand_others_cutting_ability = models.CharField('刃物台/その他/切断能力[mm×t]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_blade_length = models.IntegerField('刃物台/その他/刃の長さ[mm]', blank=True, null=True)
    spec_knife_stand_others_cutting_plate_thickness = models.CharField('刃物台/その他/切断板厚[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_shear_angle = models.CharField('刃物台/その他/シャー角', blank=True, null=True, max_length=255)
    spec_knife_stand_others_rated_capacity = models.IntegerField('刃物台/その他/定格容量[kVA]', blank=True, null=True)
    spec_knife_stand_others_allowable_usage_rate = models.FloatField('刃物台/その他/許容使用率[%]', blank=True, null=True)
    spec_knife_stand_others_welding_current = models.IntegerField('刃物台/その他/溶接電流[A]', blank=True, null=True)
    spec_knife_stand_others_standard_ffg_summary = models.CharField('刃物台/その他/標準ふところ寸法[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_future_adjustment_mechanism = models.CharField('刃物台/その他/ふところ調整機構', blank=True, null=True, max_length=255)
    spec_knife_stand_others_chip_dress_function = models.BooleanField('刃物台/その他/チップドレス機能', default=False)
    spec_knife_stand_others_electrode_weld_stroke = models.IntegerField('刃物台/その他/電極ストローク/溶接ストローク[mm]', blank=True, null=True)
    spec_knife_stand_others_electrode_horn = models.CharField('刃物台/その他/電極ホーン[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_electrode_chip_holder = models.CharField('刃物台/その他/電極チップホルダー[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_cooling_water_connection = models.CharField('刃物台/その他/冷却水接続', blank=True, null=True, max_length=255)
    spec_knife_stand_others_electrode_diameter= models.CharField('刃物台/その他/電極径×テーパー[mm×テーパー]', blank=True, null=True, max_length=255)
    spec_knife_stand_electrode_chip_shape_upper_part = models.CharField('刃物台/電極チップ形状/上部', blank=True, null=True, max_length=255)
    spec_knife_stand_electrode_chip_shape_beneath = models.CharField('刃物台/電極チップ形状/下部', blank=True, null=True, max_length=255)
    spec_knife_stand_others_primary_side_power_supply = models.CharField('刃物台/その他/1次側電源', blank=True, null=True, max_length=255)
    spec_knife_stand_others_wiring_cable = models.CharField('刃物台/その他/配線ケーブル', blank=True, null=True, max_length=255)
    spec_knife_stand_others_processing_range = models.CharField('刃物台/その他/加工範囲[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_maximum_processing_plate_thickness = models.FloatField('刃物台/その他/最大加工板厚[t]', blank=True, null=True)
    spec_knife_stand_others_welding = models.IntegerField('刃物台/その他/溶接[kVA]', blank=True, null=True)
    spec_knife_stand_others_shut_height = models.IntegerField('刃物台/その他/シャットハイト[mm]', blank=True, null=True)
    spec_knife_stand_bed_pitfall_size_left_and_right = models.IntegerField('刃物台/ベッド落とし穴寸法[mm]/左右', blank=True, null=True)
    spec_knife_stand_bed_pitfall_size_front_and_back = models.IntegerField('刃物台/ベッド落とし穴寸法[mm]/前後', blank=True, null=True)
    spec_knife_stand_others_open_back = models.IntegerField('刃物台/その他/オープンバック[mm]', blank=True, null=True)
    spec_knife_stand_stop_time_quenching_time = models.IntegerField('刃物台/停止時間/急停止時間[ms]', blank=True, null=True)
    spec_knife_stand_others_overlan_monitoring_device_position = models.IntegerField('刃物台/その他/オーバーラン監視装置の設定位置(度)', blank=True, null=True)
    spec_knife_stand_others_top_mass = models.IntegerField('刃物台/その他/上型質量[kg]', blank=True, null=True)
    spec_knife_stand_others_oscillator = models.CharField('刃物台/その他/発振器', blank=True, null=True, max_length=255)
    spec_knife_stand_others_laser_z_axis_movement_amount = models.IntegerField('刃物台/その他/レーザーZ軸移動量[mm]', blank=True, null=True)
    spec_knife_stand_others_z_axial_feed_rate = models.IntegerField('刃物台/その他/Z軸早送り速度[m/min]', blank=True, null=True)
    spec_knife_stand_others_repeat_positioning_accuracy = models.CharField('刃物台/その他/繰り返し位置決め精度[mm]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_hit_rate = models.CharField('刃物台/その他/ヒットレート[min^-1]', blank=True, null=True, max_length=255)
    spec_knife_stand_others_turret_station = models.CharField('刃物台/その他/タレットステーション', blank=True, null=True, max_length=255)


class Factory(BaseModel):
    class Meta:
        verbose_name = "工場"
        verbose_name_plural = "工場"

    def __str__(self):
        return self.name

    # CHOICES
    CHOICES_PREFECTURE = (
        (k, k) for k in (
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
            "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
            "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
            "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県", "-"
        )
    )

    # fields
    name = models.CharField("名前", max_length=255)
    detail = models.TextField("工場詳細", blank=True, null=True)
    postal_code = models.CharField('郵便番号', max_length=8, default='000-0000')
    address = models.CharField('住所', max_length=255)
    prefecture = models.CharField("都道府県", max_length=255, choices=CHOICES_PREFECTURE, blank=True, null=True)
    address1 = models.CharField("市町村区", max_length=255, blank=True, null=True)
    address2 = models.CharField("番地", max_length=255, blank=True, null=True)
    address3 = models.CharField("建物名", max_length=255, blank=True, null=True)
    mail_address = models.EmailField('メールアドレス', blank=True, null=True)
    fax_number = models.CharField('FAX', max_length=255, blank=True, null=True)
    phone_number = models.CharField('電話番号', max_length=255, blank=True, null=True)
    url = models.URLField("会社HP", blank=True, null=True)
    own_machines = models.ManyToManyField(Machine, through='OwnMachine', blank=True, 
        verbose_name='保有機械', limit_choices_to={"is_active": True},
        )


    def __str__(self):
        return self.name


class OwnMachine(BaseModel):
    class Meta:
        verbose_name = "保有機械"
        verbose_name_plural = "保有機械"

    machine = models.ForeignKey(Machine, verbose_name='機械', 
        limit_choices_to={"is_active": True}, on_delete=models.CASCADE
        )
    factory = models.ForeignKey(Factory, verbose_name='工場', 
        limit_choices_to={"is_active": True}, on_delete=models.CASCADE
        )
    num = models.IntegerField('保有数', help_text="不明な場合は1台とする", default=1)