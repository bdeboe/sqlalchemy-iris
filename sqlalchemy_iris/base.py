import datetime
from telnetlib import BINARY
from . import information_schema as ischema
from sqlalchemy import exc
from sqlalchemy.orm import aliased
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy.sql import compiler
from sqlalchemy.sql import util as sql_util
from sqlalchemy.sql import between
from sqlalchemy.sql import func
from sqlalchemy import sql
from sqlalchemy import util
from sqlalchemy import types as sqltypes

from sqlalchemy.types import BIGINT
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import INTEGER
from sqlalchemy.types import BOOLEAN
from sqlalchemy.types import DATE
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import TIME
from sqlalchemy.types import NUMERIC
from sqlalchemy.types import FLOAT
from sqlalchemy.types import VARBINARY
from sqlalchemy.types import TEXT
from sqlalchemy.types import SMALLINT

ischema_names = {
    "BIGINT": BIGINT,
    "VARCHAR": VARCHAR,
    "INTEGER": INTEGER,
    "BIT": BOOLEAN,
    "DATE": DATE,
    "TIMESTAMP": TIMESTAMP,
    "NUMERIC": NUMERIC,
    "DOUBLE": FLOAT,
    "VARBINARY": BINARY,
    "LONGVARCHAR": TEXT,
    "LONGVARBINARY": VARBINARY,
    "TIME": TIME,
    "SMALLINT": SMALLINT,
    "TINYINT": SMALLINT,
}

RESERVED_WORDS = set(
    [
        "%AFTERHAVING",
        "%ALLINDEX",
        "%ALPHAUP",
        "%ALTER",
        "%BEGTRANS",
        "%CHECKPRIV",
        "%CLASSNAME",
        "%CLASSPARAMETER",
        "%DBUGFULL",
        "%DELDATA",
        "%DESCRIPTION",
        "%EXACT",
        "%EXTERNAL",
        "%FILE",
        "%FIRSTTABLE",
        "%FLATTEN",
        "%FOREACH",
        "%FULL",
        "%ID",
        "%IDADDED",
        "%IGNOREINDEX",
        "%IGNOREINDICES",
        "%INLIST",
        "%INORDER",
        "%INTERNAL",
        "%INTEXT",
        "%INTRANS",
        "%INTRANSACTION",
        "%KEY",
        "%MATCHES",
        "%MCODE",
        "%MERGE",
        "%MINUS",
        "%MVR",
        "%NOCHECK",
        "%NODELDATA",
        "%NOFLATTEN",
        "%NOFPLAN",
        "%NOINDEX",
        "%NOLOCK",
        "%NOMERGE",
        "%NOPARALLEL",
        "%NOREDUCE",
        "%NORUNTIME",
        "%NOSVSO",
        "%NOTOPOPT",
        "%NOTRIGGER",
        "%NOUNIONOROPT",
        "%NUMROWS",
        "%ODBCIN",
        "%ODBCOUT",
        "%PARALLEL",
        "%PLUS",
        "%PROFILE",
        "%PROFILE_ALL",
        "%PUBLICROWID",
        "%ROUTINE",
        "%ROWCOUNT",
        "%RUNTIMEIN",
        "%RUNTIMEOUT",
        "%STARTSWITH",
        "%STARTTABLE",
        "%SQLSTRING",
        "%SQLUPPER",
        "%STRING",
        "%TABLENAME",
        "%TRUNCATE",
        "%UPPER",
        "%VALUE",
        "%VID",
        "ABSOLUTE",
        "ADD",
        "ALL",
        "ALLOCATE",
        "ALTER",
        "AND",
        "ANY",
        "ARE",
        "AS",
        "ASC",
        "ASSERTION",
        "AT",
        "AUTHORIZATION",
        "AVG",
        "BEGIN",
        "BETWEEN",
        "BIT",
        "BIT_LENGTH",
        "BOTH",
        "BY",
        "CASCADE",
        "CASE",
        "CAST |",
        "CHAR",
        "CHARACTER",
        "CHARACTER_LENGTH",
        "CHAR_LENGTH",
        "CHECK",
        "CLOSE",
        "COALESCE",
        "COLLATE",
        "COMMIT",
        "CONNECT",
        "CONNECTION",
        "CONSTRAINT",
        "CONSTRAINTS",
        "CONTINUE",
        "CONVERT",
        "CORRESPONDING",
        "COUNT",
        "CREATE",
        "CROSS",
        "CURRENT",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "CURRENT_USER",
        "CURSOR",
        "DATE",
        "DEALLOCATE",
        "DEC",
        "DECIMAL",
        "DECLARE",
        "DEFAULT",
        "DEFERRABLE",
        "DEFERRED",
        "DELETE",
        "DESC",
        "DESCRIBE",
        "DESCRIPTOR",
        "DIAGNOSTICS",
        "DISCONNECT",
        "DISTINCT",
        "DOMAIN",
        "DOUBLE",
        "DROP",
        "ELSE",
        "END",
        "ENDEXEC",
        "ESCAPE",
        "EXCEPT",
        "EXCEPTION",
        "EXEC",
        "EXECUTE",
        "EXISTS",
        "EXTERNAL",
        "EXTRACT",
        "FALSE",
        "FETCH",
        "FIRST",
        "FLOAT",
        "FOR",
        "FOREIGN",
        "FOUND",
        "FROM",
        "FULL",
        "GET",
        "GLOBAL",
        "GO",
        "GOTO",
        "GRANT",
        "GROUP",
        "HAVING",
        "HOUR",
        "IDENTITY",
        "IMMEDIATE",
        "IN",
        "INDICATOR",
        "INITIALLY",
        "INNER",
        "INPUT",
        "INSENSITIVE",
        "INSERT",
        "INT",
        "INTEGER",
        "INTERSECT",
        "INTERVAL",
        "INTO",
        "IS",
        "ISOLATION",
        "JOIN",
        "LANGUAGE",
        "LAST",
        "LEADING",
        "LEFT",
        "LEVEL",
        "LIKE",
        "LOCAL",
        "LOWER",
        "MATCH",
        "MAX",
        "MIN",
        "MINUTE",
        "MODULE",
        "NAMES",
        "NATIONAL",
        "NATURAL",
        "NCHAR",
        "NEXT",
        "NO",
        "NOT",
        "NULL",
        "NULLIF",
        "NUMERIC",
        "OCTET_LENGTH",
        "OF",
        "ON",
        "ONLY",
        "OPEN",
        "OPTION",
        "OR",
        "OUTER",
        "OUTPUT",
        "OVERLAPS",
        "PAD",
        "PARTIAL",
        "PREPARE",
        "PRESERVE",
        "PRIMARY",
        "PRIOR",
        "PRIVILEGES",
        "PROCEDURE",
        "PUBLIC",
        "READ",
        "REAL",
        "REFERENCES",
        "RELATIVE",
        "RESTRICT",
        "REVOKE",
        "RIGHT",
        "ROLE",
        "ROLLBACK",
        "ROWS",
        "SCHEMA",
        "SCROLL",
        "SECOND",
        "SECTION",
        "SELECT",
        "SESSION_USER",
        "SET",
        "SHARD",
        "SMALLINT",
        "SOME",
        "SPACE",
        "SQLERROR",
        "SQLSTATE",
        "STATISTICS",
        "SUBSTRING",
        "SUM",
        "SYSDATE",
        "SYSTEM_USER",
        "TABLE",
        "TEMPORARY",
        "THEN",
        "TIME",
        "TIMEZONE_HOUR",
        "TIMEZONE_MINUTE",
        "TO",
        "TOP",
        "TRAILING",
        "TRANSACTION",
        "TRIM",
        "TRUE",
        "UNION",
        "UNIQUE",
        "UPDATE",
        "UPPER",
        "USER",
        "USING",
        "VALUES",
        "VARCHAR",
        "VARYING",
        "WHEN",
        "WHENEVER",
        "WHERE",
        "WITH",
        "WORK",
        "WRITE",
    ]
)


class IRISCompiler(sql.compiler.SQLCompiler):
    """IRIS specific idiosyncrasies"""

    def limit_clause(self, select, **kw):
        return ""

    def fetch_clause(self, select, **kw):
        return ""

    def visit_empty_set_expr(self, type_):
        return "SELECT 1 WHERE 1!=1"

    def _get_limit_or_fetch(self, select):
        if select._fetch_clause is None:
            return select._limit_clause
        else:
            return select._fetch_clause

    def get_select_precolumns(self, select, **kw):

        text = ""
        if select._has_row_limiting_clause and self._use_top(select):
            text += "TOP %s " % self.process(
                self._get_limit_or_fetch(select), **kw
            )

        if select._distinct or select._distinct_on:
            if select._distinct_on:
                text += (
                    "DISTINCT ON ("
                    + ", ".join(
                        [
                            self.process(col, **kw)
                            for col in select._distinct_on
                        ]
                    )
                    + ") "
                )
            else:
                text += "DISTINCT "

        return text

    def _use_top(self, select):
        return (select._offset_clause is None) and (
            select._simple_int_clause(select._limit_clause)
            or select._simple_int_clause(select._fetch_clause)
        )

    def translate_select_structure(self, select_stmt, **kwargs):
        """Look for ``LIMIT`` and OFFSET in a select statement, and if
        so tries to wrap it in a subquery with ``row_number()`` criterion.

        """
        select = select_stmt

        if (
            select._has_row_limiting_clause
            and not self._use_top(select)
            and not getattr(select, "_iris_visit", None)
        ):
            _order_by_clauses = [
                sql_util.unwrap_label_reference(elem)
                for elem in select._order_by_clause.clauses
            ]

            limit_clause = self._get_limit_or_fetch(select)
            offset_clause = select._offset_clause

            select = select._generate()
            select._iris_visit = True
            label = "iris_rn"
            select = (
                select.add_columns(
                    sql.func.ROW_NUMBER()
                    .over(order_by=_order_by_clauses)
                    .label(label)
                )
                .order_by(None)
                .alias()
            )

            iris_rn = sql.column(label)
            limitselect = sql.select(
                *[c for c in select.c if c.key != label]
            )
            if offset_clause is not None:
                if limit_clause is not None:
                    limitselect = limitselect.where(
                        between(iris_rn, offset_clause + 1,
                                limit_clause + offset_clause)
                    )
                else:
                    limitselect = limitselect.where(iris_rn > offset_clause)
            else:
                limitselect = limitselect.where(iris_rn <= (limit_clause))
            return limitselect
        else:
            return select


class IRISDDLCompiler(sql.compiler.DDLCompiler):
    """IRIS syntactic idiosyncrasies"""

    def visit_create_schema(self, create, **kw):
        return ""

    def visit_drop_schema(self, drop, **kw):
        return ""

    def visit_check_constraint(self, constraint, **kw):
        raise exc.CompileError("Check CONSTRAINT not supported")


class IRISTypeCompiler(compiler.GenericTypeCompiler):
    def visit_boolean(self, type_, **kw):
        return "BIT"


class IRISIdentifierPreparer(sql.compiler.IdentifierPreparer):
    """Install IRIS specific reserved words."""

    reserved_words = compiler.RESERVED_WORDS.copy()
    reserved_words.update(RESERVED_WORDS)
    illegal_initial_characters = compiler.ILLEGAL_INITIAL_CHARACTERS.union(
        ["_"]
    )

    def __init__(self, dialect):
        super(IRISIdentifierPreparer, self).__init__(
            dialect, omit_schema=False)


class IRISExecutionContext(default.DefaultExecutionContext):
    pass


HOROLOG_ORDINAL = datetime.date(1840, 12, 31).toordinal()


class _IRISDate(sqltypes.Date):
    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            horolog = value.toordinal() - HOROLOG_ORDINAL
            return str(horolog)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            horolog = int(value) + HOROLOG_ORDINAL
            return datetime.date.fromordinal(horolog)

        return process


class _IRISDateTime(sqltypes.DateTime):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return value.strftime('%Y-%m-%d %H:%M:%S')
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value

        return process


class _IRISTime(sqltypes.DateTime):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return value.strftime('%H:%M:%S')
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                horolog = value
                hour = horolog // 3600
                horolog -= hour * 3600
                minute = horolog // 60
                second = horolog % 60
                return datetime.time(hour, minute, second)
            return value

        return process


colspecs = {
    sqltypes.Date: _IRISDate,
    sqltypes.DateTime: _IRISDateTime,
    sqltypes.Time: _IRISTime,
}


class IRISDialect(default.DefaultDialect):
    driver = 'iris'

    default_schema_name = "SQLUser"

    default_paramstyle = "format"

    supports_native_decimal = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = True
    supports_alter = True
    supports_schemas = True
    supports_views = True

    supports_sequences = False

    supports_statement_cache = False
    postfetch_lastrowid = False
    non_native_boolean_check_constraint = False
    supports_simple_order_by_label = False
    supports_empty_insert = False
    supports_is_distinct_from = False

    colspecs = colspecs

    ischema_names = ischema_names

    statement_compiler = IRISCompiler
    ddl_compiler = IRISDDLCompiler
    preparer = IRISIdentifierPreparer
    type_compiler = IRISTypeCompiler
    execution_ctx_cls = IRISExecutionContext

    def __init__(self, **kwargs):
        default.DefaultDialect.__init__(self, **kwargs)

    @classmethod
    def dbapi(cls):
        import iris._IRISNative as irisnative
        import iris.dbapi._DBAPI as dbapi
        dbapi.connect = irisnative.connect
        dbapi.paramstyle = "format"
        return dbapi

    def create_connect_args(self, url):
        opts = {}
        opts["hostname"] = url.host
        opts["port"] = int(url.port) if url.port else 1972
        opts["namespace"] = url.database if url.database else 'USER'
        opts["username"] = url.username if url.username else ''
        opts["password"] = url.password if url.password else ''

        return ([], opts)

    def _fix_for_params(self, query, params, many=False):
        if query.endswith(';'):
            query = query[:-1]
        if params is None:
            params = []
        elif hasattr(params, 'keys'):
            # Handle params as dict
            args = {k: "?" % k for k in params}
            query = query % args
        else:
            # Handle params as sequence
            args = ['?' for i in range(len(params if not many else params[0]))]
            query = query % tuple(args)
        newparams = list()
        for p in params:
            newparams.append(p if not many else list(p)
                             if len(p) > 1 else p[0])
        return query, newparams

    def do_execute(self, cursor, query, params, context=None):
        query, params = self._fix_for_params(query, params)
        print('do_execute', query, params)
        cursor.execute(query, params)

    def do_executemany(self, cursor, query, params, context=None):
        query, params = self._fix_for_params(query, params, True)
        print('do_execute_many', query, params)
        cursor.executemany(query, params)

    def get_schema(self, schema=None):
        if schema is None:
            return 'SQLUser'
        return schema

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        s = sql.select(ischema.schemata.c.schema_name).order_by(
            ischema.schemata.c.schema_name
        )
        schema_names = [r[0] for r in connection.execute(s)]
        return schema_names

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        tables = ischema.tables
        schema_name = self.get_schema(schema)
        s = (
            sql.select(tables.c.table_name)
            .where(
                sql.and_(
                    tables.c.table_schema == str(schema_name),
                    tables.c.table_type == "BASE TABLE",
                )
            )
            .order_by(tables.c.table_name)
        )
        table_names = [r[0] for r in connection.execute(s)]
        return table_names

    @reflection.cache
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)
        tables = ischema.tables
        schema_name = self.get_schema(schema)

        s = (
            sql.select(func.count())
            .where(
                sql.and_(
                    tables.c.table_schema == str(schema_name),
                    tables.c.table_name == str(table_name),
                )
            )
        )
        return bool(connection.execute(s).scalar())

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, unique=False, **kw):
        schema_name = self.get_schema(schema)
        indexes = ischema.indexes

        s = (
            sql.select(
                indexes.c.index_name,
                indexes.c.column_name,
                indexes.c.primary_key,
                indexes.c.non_unique,
                indexes.c.asc_or_desc,
            )
            .where(
                sql.and_(
                    indexes.c.table_schema == str(schema_name),
                    indexes.c.table_name == str(table_name),
                    indexes.c.primary_key == sql.false(),
                    (indexes.c.non_unique == sql.true()) if not unique else (1 == 1)
                )
            )
            .order_by(indexes.c.ordinal_position)
        )

        rs = connection.execute(s)

        indexes = util.defaultdict(dict)
        for row in rs:
            indexrec = indexes[row["INDEX_NAME"]]
            if "name" not in indexrec:
                indexrec["name"] = self.normalize_name(row["INDEX_NAME"])
                indexrec["column_names"] = []
                indexrec["unique"] = not row["NON_UNIQUE"]

            indexrec["column_names"].append(
                self.normalize_name(row["COLUMN_NAME"])
            )

        indexes = list(indexes.values())
        return indexes

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        schema_name = self.get_schema(schema)
        key_constraints = ischema.key_constraints
        constraints = ischema.constraints

        s = (
            sql.select(
                key_constraints.c.constraint_name,
                key_constraints.c.column_name,
            )
            .join(constraints,
                  sql.and_(
                      key_constraints.c.constraint_name == constraints.c.constraint_name,
                      key_constraints.c.table_schema == constraints.c.table_schema,
                  )
                  )
            .where(
                sql.and_(
                    key_constraints.c.table_schema == str(schema_name),
                    key_constraints.c.table_name == str(table_name),
                    constraints.c.constraint_type == "PRIMARY KEY",
                )
            )
            .order_by(key_constraints.c.ordinal_position)
        )

        rs = connection.execute(s)

        constraint_name = None
        pkfields = []
        for row in rs:
            constraint_name = self.normalize_name(row["CONSTRAINT_NAME"])
            pkfields.append(self.normalize_name(row["COLUMN_NAME"]))

        if pkfields:
            return {
                "constrained_columns": pkfields,
                "name": constraint_name,
            }

        return None

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        indexes = self.get_indexes(
            connection, table_name, schema, unique=True, **kw)
        return [{'name': i['name'], 'column_names': i['column_names']}
                for i in indexes if i['unique']]

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        schema_name = self.get_schema(schema)
        ref_constraints = ischema.ref_constraints
        key_constraints = ischema.key_constraints
        key_constraints_ref = aliased(ischema.key_constraints)

        s = (
            sql.select(
                key_constraints.c.constraint_name,
                key_constraints.c.column_name,
                key_constraints_ref.c.table_schema,
                key_constraints_ref.c.table_name,
                key_constraints_ref.c.column_name,
                ref_constraints.c.match_option,
                ref_constraints.c.update_rule,
                ref_constraints.c.delete_rule,
            )
            .join(
                key_constraints,
                sql.and_(
                    key_constraints.c.table_schema == ref_constraints.c.constraint_schema,
                    key_constraints.c.constraint_name == ref_constraints.c.constraint_name,
                )
            )
            .join(
                key_constraints_ref,
                sql.and_(
                    key_constraints_ref.c.constraint_schema == ref_constraints.c.unique_constraint_schema,
                    key_constraints_ref.c.constraint_name == ref_constraints.c.unique_constraint_name,
                    key_constraints_ref.c.ordinal_position == key_constraints.c.ordinal_position,
                )
            )
            .where(
                sql.and_(
                    key_constraints.c.table_schema == str(schema_name),
                    key_constraints.c.table_name == str(table_name),
                )
            )
            .order_by(key_constraints_ref.c.ordinal_position)
        )

        rs = connection.execute(s)

        fkeys = []

        def fkey_rec():
            return {
                "name": None,
                "constrained_columns": [],
                "referred_schema": None,
                "referred_table": None,
                "referred_columns": [],
                "options": {},
            }

        fkeys = util.defaultdict(fkey_rec)

        for row in rs:
            (
                rfknm,
                scol,
                rschema,
                rtbl,
                rcol,
                _,  # match rule
                fkuprule,
                fkdelrule,
            ) = row

            rec = fkeys[rfknm]
            rec["name"] = rfknm

            if fkuprule != "NO ACTION":
                rec["options"]["onupdate"] = fkuprule

            if fkdelrule != "NO ACTION":
                rec["options"]["ondelete"] = fkdelrule

            if not rec["referred_table"]:
                rec["referred_table"] = rtbl
                if rschema != 'SQLUser':
                    rec["referred_schema"] = rschema

            local_cols, remote_cols = (
                rec["constrained_columns"],
                rec["referred_columns"],
            )

            local_cols.append(scol)
            remote_cols.append(rcol)

        if fkeys:
            return list(fkeys.values())

        return []

    def get_columns(self, connection, table_name, schema=None, **kw):
        schema_name = self.get_schema(schema)
        columns = ischema.columns

        whereclause = sql.and_(
            columns.c.table_name == str(table_name),
            columns.c.table_schema == str(schema_name),
        )

        s = (
            sql.select(
                columns.c.column_name,
                columns.c.data_type,
                columns.c.is_nullable,
                columns.c.character_maximum_length,
                columns.c.numeric_precision,
                columns.c.numeric_scale,
                columns.c.column_default,
                columns.c.collation_name,
                columns.c.auto_increment,
                # columns.c.description,
            )
            .select_from(columns)
            .where(whereclause)
            .order_by(columns.c.ordinal_position)
        )

        c = connection.execution_options(future_result=True).execute(s)

        cols = []
        for row in c.mappings():
            name = row[columns.c.column_name]
            type_ = row[columns.c.data_type].upper()
            nullable = row[columns.c.is_nullable] == "YES"
            charlen = row[columns.c.character_maximum_length]
            numericprec = row[columns.c.numeric_precision]
            numericscale = row[columns.c.numeric_scale]
            default = row[columns.c.column_default]
            collation = row[columns.c.collation_name]
            autoincrement = row[columns.c.auto_increment]
            # description = row[columns.c.description]

            coltype = self.ischema_names.get(type_, None)

            kwargs = {}
            if coltype in (
                VARCHAR,
                BINARY,
                TEXT,
                VARBINARY,
            ):
                if charlen == -1:
                    charlen = None
                kwargs["length"] = charlen
                if collation:
                    kwargs["collation"] = collation
            if coltype is None:
                util.warn(
                    "Did not recognize type '%s' of column '%s'"
                    % (type_, name)
                )
                coltype = sqltypes.NULLTYPE
            else:
                if issubclass(coltype, sqltypes.Numeric):
                    kwargs["precision"] = numericprec

                    if not issubclass(coltype, sqltypes.Float):
                        kwargs["scale"] = numericscale

                coltype = coltype(**kwargs)

            cdict = {
                "name": name,
                "type": coltype,
                "nullable": nullable,
                "default": default,
                "autoincrement": autoincrement,
                # "comment": description,
            }
            cols.append(cdict)

        if cols:
            return cols

        return None

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        schema_name = self.get_schema(schema)
        views = ischema.views
        s = (
            sql.select(views.c.table_name)
            .where(
                views.c.table_schema == str(schema_name),
            )
            .order_by(views.c.table_name)
        )
        view_names = [r[0] for r in connection.execute(s)]
        return view_names

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        schema_name = self.get_schema(schema)
        views = ischema.views

        view_def = connection.execute(
            sql.select(views.c.view_definition)
            .where(
                views.c.table_schema == str(schema_name),
                views.c.table_name == str(view_name),
            )
        ).scalar()

        if view_def:
            return view_def
        return None