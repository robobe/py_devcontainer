import cv2
import hydra
# from omegaconf import DictConfig, OmegaConf
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass


@dataclass
class DB:
    driver: str
    table: str
    user: str
    password: str


@dataclass
class Settings:
    db: DB


cs = ConfigStore.instance()
# name `base_config` is used for matching it with the main.yaml's default section
cs.store(name="base_config", node=Settings)


@hydra.main(config_path=".", config_name="config", version_base="1.1")
def my_app(cfg: Settings) -> None:
    # print(OmegaConf.to_yaml(cfg))
    # print(f"reading data with username {cfg.user}")
    print(cfg)
    print(type(cfg))
    print(cfg.db.driver)
    print(cfg.db.table)


def main():
    img = cv2.imread("/home/user/data/opencv-logo.png", 0)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    my_app()
