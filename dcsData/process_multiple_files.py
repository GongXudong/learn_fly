import json
import os


def main():
    with open('process_config.json', 'r', encoding='utf-8') as f:
        configs = json.load(f)

    for cfg in configs:
        print(cfg)
        for skip in cfg['goal_skips']:
            cur_cmd = f"python process_single_file.py {cfg['csv_file']} --aircraft_id {cfg['aircraft_id']} --goal_skip {skip} --output_dir {cfg['output_dir']}"
            print(cur_cmd)
            os.system(cur_cmd)


if __name__ == '__main__':
    main()
