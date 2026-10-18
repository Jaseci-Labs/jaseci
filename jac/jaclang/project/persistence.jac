obj PersistenceConfig {
    has namespace: str = "main";

    def module_facts(module: str) -> tuple[str, str];
}

def parse_persistence(raw: any, project_name: str) -> PersistenceConfig;

impl PersistenceConfig.module_facts(module: str) -> tuple[str, str] {
    return (self.namespace, module);
}

impl parse_persistence(raw: any, project_name: str) -> PersistenceConfig {
    return PersistenceConfig(namespace=persistence_namespace(raw, project_name));
}
