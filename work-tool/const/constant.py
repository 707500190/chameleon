
type_mapping = {
    'int': ('Integer', ''),
    'bigint': ('Long', ''),
    'float': ('Float', ''),
    'double': ('Double', ''),
    'decimal': ('BigDecimal', 'java.math'),
    'varchar': ('String', ''),
    'text': ('String', ''),
    'datetime': ('Date', 'java.util'),
    'timestamp': ('Timestamp', 'java.sql'),
    # 其他字段类型的映射定义
}
