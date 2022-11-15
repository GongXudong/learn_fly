import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='')
parser.add_argument('csv_file', type=str, help='要处理的csv文件名')
parser.add_argument('--aircraft_id', type=str, default='201', help='要抽取数据的飞机id')
parser.add_argument('--goal_skip', type=int, default=10, help='以多少个step后的点作为目标')
parser.add_argument('--output_dir', type=str, default='processed_data', help='输出目录')


args = parser.parse_args()

base_path = Path().cwd()
csv_file_path = base_path / Path(args.csv_file)


def check_args():

    # print(args.csv_file)
    # print(args.goal_skip)
    # print(args.aircraft_id)
    # print(args.output_dir)

    # if not os.path.exists(str(csv_file_path)):
    if not csv_file_path.is_file():
        raise FileNotFoundError("csv file not found!")


check_args()


def read_csv_file():
    # with open(str(csv_file_path), encoding='utf-8') as f:
    #     data = np.loadtxt(f, delimiter=',', skiprows=1, usecols=[])
    df = pd.read_csv(csv_file_path.resolve())
    df = df.astype({'Id': 'str'})
    return df[df['Id'] == args.aircraft_id][['Longitude', 'Latitude', 'Altitude', 'Roll', 'Pitch', 'Yaw', 'Throttle', 'RollControlPosition', 'PitchControlPosition', 'YawControlPosition']]
    # return df[(df['Id'] == args.aircraft_id) & (df['RollControlPosition'] > 0)][['Longitude', 'Latitude', 'Altitude', 'Roll', 'Pitch', 'Yaw', 'Throttle', 'RollControlPosition', 'PitchControlPosition', 'YawControlPosition']]


def main():
    df = read_csv_file()
    arr = np.array(df)
    print(arr.shape)

    arr1 = np.array([[*arr[i], *arr[i + args.goal_skip][:6], args.goal_skip] for i in range(len(arr) - args.goal_skip)])
    print(arr1.shape)

    output_dir_path = base_path / Path(args.output_dir)
    # 检查输出目录是否存在，如不存在，则创建输出目录
    if not output_dir_path.is_dir():
        Path.mkdir(output_dir_path)

    output_file_path = output_dir_path / (csv_file_path.stem + "_skip_" + str(args.goal_skip) + csv_file_path.suffix)

    column_names = [
        'Longitude', 'Latitude', 'Altitude', 'Roll', 'Pitch', 'Yaw',
        'Throttle', 'RollControlPosition', 'PitchControlPosition', 'YawControlPosition',
        'GoalLongitude', 'GoalLatitude', 'GoalAltitude', 'GoalRoll', 'GoalPitch', 'GoalYaw', 'GoalSkip']
    processed_data_df = pd.DataFrame(data=arr1, columns=column_names)
    processed_data_df.to_csv(output_file_path.resolve(), sep=',', index=False)


if __name__ == '__main__':
    main()
