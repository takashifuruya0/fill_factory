# Generated by Django 3.2.5 on 2022-05-30 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0003_auto_20220531_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_atc_arm_driving_motor',
            field=models.IntegerField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/ATCアーム駆動用モータ[W]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_magazine_turning_drive_motor',
            field=models.IntegerField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/マガジン旋回駆動用モータ[W]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_pullstad_call_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/プルスタッド(呼び番号)'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_maximum_diameter_with_adjacent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具最大径(隣接工具あり)[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_maximum_diameter_without_adjacent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具最大径(隣接工具なし)[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_maximum_length',
            field=models.IntegerField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具最大長さ(ゲージラインより)[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_maximum_mass',
            field=models.IntegerField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具最大質量(モーメント)[kg(N・m)]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_replacement_method',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具交換方式'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_replacement_time_cut2cut',
            field=models.FloatField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具交換時間\u3000カット・ツー・カット[s]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_replacement_time_tool_to_tool',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具交換時間\u3000ツール・ツー・ツール[s]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_selection_method',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具選択方式'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_shank_call_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='自動工具交換装置(ATC)/その他/ツールシャンク(呼び番号)'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_atc_others_tool_storage_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='自動工具交換装置(ATC)/その他/工具収納本数'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_palette_others_index_angle',
            field=models.IntegerField(blank=True, null=True, verbose_name='パレット/その他/割り出し角度[°]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_palette_others_maximum_load_mass',
            field=models.IntegerField(blank=True, null=True, verbose_name='パレット/その他/最大積載質量[kg]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_palette_others_maximum_loading_work_dimension',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='パレット/その他/最大積載ワーク寸法[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_palette_work_surface_size_horizontal',
            field=models.IntegerField(blank=True, null=True, verbose_name='パレット/作業面の大きさ/横[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_palette_work_surface_size_vertical',
            field=models.IntegerField(blank=True, null=True, verbose_name='パレット/作業面の大きさ/縦[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_fast_forward_speed_x',
            field=models.IntegerField(blank=True, null=True, verbose_name='送り速度/早送り速度[m/min]/X'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_fast_forward_speed_y',
            field=models.IntegerField(blank=True, null=True, verbose_name='送り速度/早送り速度[m/min]/Y'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_fast_forward_speed_yl',
            field=models.IntegerField(blank=True, null=True, verbose_name='送り速度/早送り速度[m/min]/YL'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_fast_forward_speed_z',
            field=models.IntegerField(blank=True, null=True, verbose_name='送り速度/早送り速度[m/min]/Z'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_others_average_continuous_cutting_feed_rate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り速度/その他/平均連続切削送り速度(X,Y,Z)[mm/min]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_others_cutting_feed_rate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り速度/その他/切削送り速度[mm/min]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_others_jog_feed_rate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り速度/その他/ジョグ送り速度[mm/min]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_others_manual_feed_rate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り速度/その他/手動送り速度[mm/min]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_sending_speed_others_w_axis_feed_rate',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り速度/その他/W軸送り速度[mm/min]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_base_rotation_speed',
            field=models.IntegerField(blank=True, null=True, verbose_name='主軸/その他/基底回転数[min^-1]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_bearing_internal_diameter',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/軸受内径[mm]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_maximum_torque',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/最大トルク[N・m]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_rotational_speed_range_transform_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/回転速度域変換数'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_air_blowing_device',
            field=models.BooleanField(default=False, verbose_name='主軸/その他/主軸エアブロー装置'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_end_nose_shape',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/主軸端ノーズ形状'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_quota_stop_device',
            field=models.BooleanField(default=False, verbose_name='主軸/その他/主軸定位置停止装置'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_rotational_speed',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/主軸回転速度[min^-1]'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_taper',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主軸/その他/主軸テーパ'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spindle_through_hole_diameter',
            field=models.IntegerField(blank=True, null=True, verbose_name='主軸/その他/主軸貫通穴径'),
        ),
        migrations.AddField(
            model_name='machine',
            name='spec_spindle_others_spool_diameter',
            field=models.IntegerField(blank=True, null=True, verbose_name='主軸/その他/主軸径'),
        ),
    ]
