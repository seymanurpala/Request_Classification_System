import config


class TaskValidator:

    def validateTaskType(self, tip: str, alan: str, selectableTaskTypeNames: set[str]) -> None:
        if tip and tip not in selectableTaskTypeNames:
            raise ValueError(f"Gecersiz {alan}: {tip}")

    def validateRequiredText(self, value: str, alan: str, minLength: int = 1) -> None:
        if not value or not value.strip():
            raise ValueError(f"{alan} bos olamaz.")
        if len(value.strip()) < minLength:
            raise ValueError(f"{alan} cok kisa.")

    def validateGelisKanali(self, gelisKanali: str) -> None:
        if gelisKanali not in set(config.VALID_CHANNELS):
            raise ValueError(f"Gecersiz gelis kanali: {gelisKanali}")

    def validateCreateTaskData(self, data: dict, selectableTaskTypeNames: set[str]) -> None:
        for key, label, minLength in [
            ("talepMetni", "Talep metni", 3),
            ("vatandasAdi", "Vatandas adi", 2),
            ("ilce", "Ilce", 1),
            ("gelisKanali", "Gelis kanali", 1),
        ]:
            self.validateRequiredText(data[key], label, minLength=minLength)

        self.validateGelisKanali(data["gelisKanali"])

        if data.get("manuelTip"):
            self.validateTaskType(data["manuelTip"], "talep tipi", selectableTaskTypeNames)
