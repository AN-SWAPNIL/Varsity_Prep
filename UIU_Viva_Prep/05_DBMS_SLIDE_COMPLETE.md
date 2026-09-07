# Bismillah.

# Database Management Systems — Slide-Complete Viva Recall

This chapter was re-audited against the **current main DBMS slides only**:

| Current source | Pages | Main coverage |
|---|---:|---|
| `DBMS_Ashik_Sir_merged.pdf` | 559 | DBMS foundations, relational model, SQL, relational algebra, ER/EER design, functional dependencies, normalization |
| `DBMS_Toufiq_Sir_merged.pdf` | 337 | storage, records and files, indexing, query processing and optimization, transactions, concurrency control |
| **Total** | **896** | **logical design through physical execution and transaction processing** |

The merged PDFs supersede the old individual-deck/archive inventory. SQL examples below are retained as course-style recall exercises; they are not claimed to be outputs from files that are no longer in the academic folder.

## How to use this chapter

- **[SLIDE]** means the point is directly taught in the supplied lecture material.
- **[COURSE EXAMPLE]** marks an executable example based on a schema used in the course material.
- **[CORE SUPPLEMENT]** means it is standard DBMS knowledge added because it is viva-important but absent or only named in the supplied slides.
- **[CORRECTION]** flags a slide-era, vendor-specific, ambiguous, or erroneous statement so that you do not repeat it uncritically.
- Read the **30-second answer** first. Then expand only if the panel asks “why?”, “how?”, or asks for an example.
- For an algorithm question, give: **idea → invariant → steps → worked trace → cost → limitation**.

---

# 1. The DBMS Mental Model

## 1.1 Thirty-second answer

A **database** is an organized collection of related, persistent data. A **DBMS** is software that defines, stores, queries, updates, protects, recovers, and coordinates access to that data. Compared with raw files or spreadsheets, a DBMS provides a schema, declarative queries, integrity constraints, transactions, concurrency control, recovery, authorization, and physical data independence.

## 1.2 Why not keep everything in files?

**[SLIDE]** A file-based solution becomes difficult when data is large, many applications share it, schemas evolve, queries vary, or failures occur.

| Problem | DBMS response |
|---|---|
| Repeated data and inconsistency | schema design and normalization |
| Hard-coded access paths | declarative SQL and optimizer |
| Two users overwrite each other | transactions and concurrency control |
| A transfer stops halfway | atomicity and recovery |
| Different users need different access | users, roles, privileges, views |
| Data layout changes break programs | physical data independence |
| Hardware/system crash | log, checkpoint, undo/redo, backup |
| Ad hoc search over large data | indexes and physical query algorithms |

Classic failure examples:

- **Lost update:** T1 and T2 both read balance 100; each computes a new value; the later write overwrites the earlier one.
- **Inconsistent read:** one transaction reads A after debit but B before credit.
- **Partial failure:** debit succeeds but credit does not.

## 1.3 Core terminology

- **Data:** recorded facts.
- **Database:** persistent collection of related data.
- **DBMS:** programs that manage databases.
- **Database system:** database + DBMS + applications/users/hardware.
- **Schema (intension):** structure and constraints; changes relatively rarely.
- **Instance/state (extension):** current rows; changes frequently.
- **Metadata:** data about data—table/column names, types, constraints, indexes, statistics, users. It is stored in the **system catalog/data dictionary**.
- **DDL:** defines structure: CREATE, ALTER, DROP.
- **DML:** queries and changes data: SELECT, INSERT, UPDATE, DELETE.
- **Declarative language:** state *what* result is wanted, not the exact access algorithm.

## 1.4 Three-schema architecture and data independence

**[SLIDE + CORE DETAIL]**

1. **External/view level:** user-specific views.
2. **Conceptual/logical level:** global relations, attributes, relationships, constraints.
3. **Internal/physical level:** files, pages, indexes, placement, compression.

- **Physical data independence:** change storage/indexing without changing logical schema or applications. This is the common and easier form.
- **Logical data independence:** change logical schema while preserving external views/programs. Harder.

Example: adding a B+ tree changes the internal level but not the SQL query. Splitting one logical table may require compatibility views to preserve external schemas.

## 1.5 Client/server access

**[SLIDE]** Applications commonly communicate with the DBMS through drivers such as **JDBC** or **ODBC**. The application sends SQL; the server parses, optimizes, executes, and returns results.

## 1.6 Relational versus non-relational

**[SLIDE]**

- A **relational database** represents data as relations/tables with rows and named columns; keys identify rows and constraints connect tables.
- Non-relational systems may use key–value, document (JSON/XML), wide-column, or graph models.

Do not answer “NoSQL has no schema.” Better: many NoSQL systems permit a flexible or application-enforced schema; they still have data shape and constraints, but may not enforce them relationally.

---

# 2. The Relational Model

## 2.1 Relation vocabulary

For schema Product(PName, Price, Category, Manufacturer):

- **Relation schema:** name plus attributes.
- **Relation instance:** current set of tuples.
- **Tuple:** one row/record.
- **Attribute:** named column.
- **Domain:** permitted atomic values for an attribute.
- **Degree/arity:** number of attributes.
- **Cardinality:** number of tuples.

In the mathematical relational model:

- a relation is a **set**, so duplicate tuples do not exist;
- tuples are unordered;
- attribute order is irrelevant under the named perspective;
- values are atomic in 1NF.

In SQL, query results are normally **bags/multisets**, so duplicates can occur unless DISTINCT or a duplicate-eliminating set operation is used.

## 2.2 Keys—say these precisely

- **Superkey:** any attribute set that uniquely identifies every possible tuple.
- **Candidate key:** a **minimal** superkey; remove any attribute and uniqueness is lost.
- **Primary key:** candidate key chosen as the main identifier.
- **Alternate key:** candidate key not chosen as primary.
- **Composite key:** key containing multiple attributes.
- **Foreign key:** attributes in one relation whose non-NULL values must match a candidate/primary key in a referenced relation.
- **Surrogate key:** artificial identifier such as an auto-generated integer.
- **Prime attribute:** belongs to at least one candidate key.

“Minimal” means minimal by **set inclusion**, not necessarily fewest bytes.

Example:

Movie(title, year, length, genre)

Two films can share a title and many films share a year, but (title, year) may uniquely identify a film. Then:

- (title, year) is a candidate key;
- (title, year, genre) is a superkey but not a candidate key;
- title alone is not a key.

## 2.3 PRIMARY KEY versus UNIQUE

**[SLIDE]**

- A table has at most one PRIMARY KEY constraint, although it can contain several columns.
- Primary-key columns are unique and NOT NULL.
- A table may have multiple UNIQUE constraints.
- NULL behavior under UNIQUE is DBMS-specific in detail; Oracle permits multiple NULLs because NULLs are not equal.

These are not equivalent:

~~~sql
UNIQUE (name),
UNIQUE (address)
~~~

and:

~~~sql
UNIQUE (name, address)
~~~

The first makes each column independently unique. The second makes only the pair unique.

## 2.4 Domains and common Oracle-oriented types

**[SLIDE]**

- CHAR(n): fixed-length; Oracle blank-pads to length n.
- VARCHAR2(n): variable-length Oracle string type. The slides sometimes say VARCHAR; VARCHAR2 is the safe Oracle choice.
- INTEGER/INT, REAL, FLOAT.
- NUMBER(p,s): p total significant decimal digits, s digits to the right of the decimal. Negative s rounds to the left.
- DATE: date/time value in Oracle's DATE type.

For input 7,456,123.89:

| Type | Effect |
|---|---|
| NUMBER(9) | rounds to 7,456,124 |
| NUMBER(9,1) | 7,456,123.9 |
| NUMBER(9,2) | 7,456,123.89 |
| NUMBER(7,-2) | rounds to 7,456,100 |
| NUMBER(6) | rejected: too many digits |

**Viva trap:** CHAR is not universally “faster” than VARCHAR. CHAR is appropriate for truly fixed-width values; VARCHAR2 usually avoids padding and storage waste. Choose by semantics and workload, not a slogan.

## 2.5 Date handling

**[SLIDE, Oracle]**

~~~sql
TO_DATE('1994-10-21', 'YYYY-MM-DD')
TO_DATE('1994-OCT-21', 'YYYY-MON-DD')
TO_CHAR(birth, 'DD-MON-YYYY')
~~~

Common masks: MM, MON, MONTH, DD, DY, YYYY, YY, RR. RR maps two-digit years into a window around 1950–2049 in the slide-era Oracle behavior.

In Oracle, subtracting two DATE values yields the number of days. Date arithmetic is vendor-specific, so state the DBMS if asked.

## 2.6 NULL and three-valued logic

NULL can mean unknown, unavailable, inapplicable, or not yet recorded. It is not 0, an empty string in general SQL, or a value equal to itself.

Any ordinary comparison with NULL evaluates to **UNKNOWN**:

~~~sql
salary = NULL      -- wrong; result is UNKNOWN
salary IS NULL    -- correct
salary IS NOT NULL
~~~

Truth table:

| p | q | p AND q | p OR q |
|---|---|---|---|
| T | T | T | T |
| T | U | U | T |
| T | F | F | T |
| U | U | U | U |
| U | F | F | U |
| F | F | F | F |

NOT T = F, NOT F = T, NOT U = U.

WHERE retains only rows for which the predicate is **TRUE**; FALSE and UNKNOWN are discarded.

Therefore this does not return rows whose age is NULL:

~~~sql
SELECT *
FROM Person
WHERE age < 25 OR age >= 25;
~~~

Use:

~~~sql
WHERE age < 25 OR age >= 25 OR age IS NULL
~~~

Arithmetic involving NULL normally yields NULL. Aggregates ignore NULL except COUNT(*):

~~~sql
COUNT(*)       -- rows, including rows with all selected fields NULL
COUNT(mark)    -- non-NULL mark values
AVG(mark)      -- average of non-NULL marks
~~~

**Critical trap—NOT IN and NULL:** if a subquery returns NULL, x NOT IN (...) can become UNKNOWN for every x. Prefer NOT EXISTS for a NULL-safe anti-join.

---

# 3. SQL from Definition to Query

## 3.1 Categories

- **DDL:** CREATE, ALTER, DROP, TRUNCATE.
- **DML:** SELECT, INSERT, UPDATE, DELETE, MERGE.
- **DCL:** GRANT, REVOKE.
- **TCL:** COMMIT, ROLLBACK, SAVEPOINT.

SQL keywords and unquoted identifiers are case-insensitive in the slide examples; string data is case-sensitive under the relevant collation. Character/string literals use single quotes.

## 3.2 Creating and inspecting tables

~~~sql
CREATE TABLE Students (
    sid       CHAR(10),
    name      VARCHAR2(50),
    email     VARCHAR2(100),
    gpa       NUMBER(3,2),
    dob       DATE,
    username  VARCHAR2(20) UNIQUE,
    CONSTRAINT students_pk PRIMARY KEY (sid)
);

DESCRIBE Students;
~~~

**[SLIDE, Oracle SQL*Plus]** USER_TABLES lists a user's tables. DROP TABLE removes a table definition and data.

### CTAS

~~~sql
CREATE TABLE LaptopCopy AS
SELECT *
FROM Laptop;
~~~

CTAS copies the selected data and inferred columns, but generally does **not** reproduce primary/foreign keys, indexes, triggers, privileges, or all defaults. Verify metadata instead of assuming a complete clone.

## 3.3 Basic SELECT

~~~sql
SELECT [DISTINCT] expression_list
FROM table_expression
WHERE row_condition
GROUP BY grouping_columns
HAVING group_condition
ORDER BY ordering_expression [ASC | DESC];
~~~

Conceptual logical evaluation order:

1. FROM and JOIN/ON
2. WHERE
3. GROUP BY
4. HAVING
5. SELECT expressions
6. DISTINCT
7. ORDER BY
8. row limiting

This explains why a SELECT alias often cannot be used in WHERE: WHERE is logically evaluated earlier.

## 3.4 Projection, duplicates, and aliases

~~~sql
SELECT category
FROM Product;                 -- duplicates retained

SELECT DISTINCT category
FROM Product;                 -- duplicates removed

SELECT product, day, price * quantity AS sales
FROM Purchase;
~~~

SQL SELECT is not exactly relational-algebra selection. In conventional terminology:

- WHERE performs **selection** of rows.
- SELECT column list performs **projection**.

## 3.5 Predicates

~~~sql
WHERE price > 100
WHERE price BETWEEN 100 AND 200       -- inclusive at both ends
WHERE year IN (1984, 1996)
WHERE category = 'Household'
WHERE condition1 AND condition2
WHERE condition1 OR condition2
WHERE NOT condition
~~~

Operator precedence: NOT, then AND, then OR. Use parentheses whenever intent could be misunderstood.

## 3.6 LIKE pattern matching

- % matches zero or more characters.
- _ matches exactly one character.

~~~sql
WHERE pname LIKE '%mo%'          -- contains "mo"
WHERE pname LIKE '%Touch'        -- ends with Touch
WHERE maker LIKE 'G_z_oWorks'
WHERE maker NOT LIKE '%mo%'
~~~

Escaping:

~~~sql
WHERE company_name LIKE '%''s%'                 -- apostrophe
WHERE interest_rate LIKE '%\%' ESCAPE '\'       -- literal %
WHERE country LIKE '%\_%' ESCAPE '\'            -- literal _
~~~

**[SLIDE, Oracle CHAR trap]** Equality comparisons may use blank-padding rules for CHAR, whereas LIKE performs pattern matching without the same padding behavior. CHAR versus VARCHAR2 can therefore change a result.

## 3.7 ORDER BY

~~~sql
SELECT pname, price, manufacturer
FROM Product
WHERE category = 'Gadgets'
ORDER BY price ASC, pname DESC;
~~~

Each ordering term has its own direction. The second breaks ties in the first. Oracle supports NULLS FIRST and NULLS LAST:

~~~sql
ORDER BY price ASC NULLS LAST
~~~

Without ORDER BY, result order is not guaranteed.

---

# 4. Queries over Multiple Tables

## 4.1 Cartesian product and join

~~~sql
SELECT *
FROM R, S;
~~~

produces every R tuple paired with every S tuple: |R × S| = |R||S|.

An old-style equijoin filters that product:

~~~sql
SELECT *
FROM Product p, Company c
WHERE p.manufacturer = c.cname;
~~~

Preferred explicit form:

~~~sql
SELECT p.pname, p.price
FROM Product p
JOIN Company c
  ON c.cname = p.manufacturer
WHERE c.country = 'Japan'
  AND p.price < 200;
~~~

**Viva trap:** forgetting the join condition creates a Cartesian product.

## 4.2 Qualification and self-join

Qualify ambiguous names:

~~~sql
SELECT p.pname, c.address
FROM Person p
JOIN Company c ON p.worksfor = c.cname;
~~~

**[SLIDE, Oracle]** A table alias is normally written without AS:

~~~sql
FROM Person p, Company c
~~~

A self-join uses two tuple variables:

~~~sql
SELECT x.pname, y.pname, x.address
FROM Person x
JOIN Person y
  ON x.address = y.address
 AND x.pname < y.pname;
~~~

Using < rather than <> returns each unordered pair once and excludes self-pairs.

## 4.3 NATURAL JOIN—know it, use cautiously

NATURAL JOIN equates **every same-named column** and keeps one copy of each common column:

~~~sql
SELECT *
FROM Product NATURAL JOIN PC;
~~~

It is concise but fragile: adding an unrelated same-named column silently changes the join. Production code normally prefers JOIN ... ON or JOIN ... USING.

## 4.4 Inner and outer joins

Given PC makers A, B, C and Laptop makers A, B, D:

- INNER JOIN returns A, B matches.
- PC LEFT OUTER JOIN Laptop returns matches plus PC's dangling C row padded with NULLs.
- PC RIGHT OUTER JOIN Laptop returns matches plus Laptop's dangling D row.
- FULL OUTER JOIN returns A, B, C, D sides, padding unmatched attributes.

~~~sql
-- Makers of PCs but not laptops: anti-join
SELECT DISTINCT p.maker
FROM PC p
LEFT JOIN Laptop l ON l.maker = p.maker
WHERE l.maker IS NULL;
~~~

Equivalent NULL-safe form:

~~~sql
SELECT DISTINCT p.maker
FROM PC p
WHERE NOT EXISTS (
    SELECT 1
    FROM Laptop l
    WHERE l.maker = p.maker
);
~~~

To return a maker from either side of a full join:

~~~sql
SELECT DISTINCT COALESCE(p.maker, l.maker) AS maker
FROM PC p
FULL OUTER JOIN Laptop l ON l.maker = p.maker;
~~~

**[CORRECTION]** Selecting only PC.maker from an unmatched Laptop row yields NULL; an OR predicate does not repair the projected value. Use COALESCE or UNION.

## 4.5 Set operations and bag behavior

Inputs must be union-compatible: same number of columns and compatible corresponding types.

~~~sql
SELECT maker FROM Product WHERE type = 'pc'
UNION
SELECT maker FROM Product WHERE type = 'laptop';

SELECT maker FROM Product WHERE type = 'pc'
INTERSECT
SELECT maker FROM Product WHERE type = 'laptop';

SELECT maker FROM Product WHERE type = 'laptop'
MINUS
SELECT maker FROM Product WHERE type = 'pc';   -- Oracle name
~~~

UNION, INTERSECT, and MINUS/EXCEPT remove duplicates. UNION ALL retains them.

For multiplicities a and b:

- UNION ALL: a + b
- INTERSECT ALL: min(a,b)
- EXCEPT ALL: max(0,a-b)

**[SLIDE-ERA NOTE]** The supplied Oracle deck says only UNION ALL is supported among the ALL variants. Treat exact support as version-specific.

---

# 5. Aggregation and Grouping

## 5.1 Aggregate functions

SUM, COUNT, MIN, MAX, AVG operate over a group. COUNT(*) counts rows; the others ignore NULL input values.

~~~sql
SELECT SUM(price * quantity) AS total_sales
FROM Purchase;
~~~

COUNT applies to duplicates unless DISTINCT is requested:

~~~sql
COUNT(category)
COUNT(DISTINCT category)
~~~

## 5.2 GROUP BY

~~~sql
SELECT product, SUM(price * quantity) AS total_sales
FROM Purchase
WHERE day > DATE '2005-10-04'
GROUP BY product;
~~~

Logical process:

1. build FROM result;
2. apply WHERE to individual rows;
3. partition surviving rows by GROUP BY values;
4. calculate one aggregate result per group;
5. apply HAVING to groups;
6. form SELECT output.

Every selected expression must normally be:

- a grouping column,
- an aggregate,
- or, in DBMSs that infer it, functionally dependent on grouping columns.

Portable viva answer: “A nonaggregated selected column must appear in GROUP BY.”

## 5.3 WHERE versus HAVING

~~~sql
SELECT product, SUM(price * quantity) AS sales
FROM Purchase
WHERE day > DATE '2005-10-04'      -- filters rows before grouping
GROUP BY product
HAVING SUM(quantity) >= 30;        -- filters complete groups
~~~

Push a nonaggregate predicate into WHERE where possible; it reduces data earlier.

## 5.4 Worked slide-style queries

~~~sql
-- Makers with at least three PC models
SELECT maker
FROM Product
WHERE type = 'pc'
GROUP BY maker
HAVING COUNT(DISTINCT model) >= 3;

-- Makers producing all three product types
SELECT maker
FROM Product
GROUP BY maker
HAVING COUNT(DISTINCT type) = 3;

-- Makers producing one type but multiple models
SELECT maker
FROM Product
GROUP BY maker
HAVING COUNT(DISTINCT type) = 1
   AND COUNT(DISTINCT model) > 1;

-- Maximum PC price for each maker that sells PCs
SELECT p.maker, MAX(pc.price) AS max_pc_price
FROM Product p
JOIN PC pc ON pc.model = p.model
GROUP BY p.maker;
~~~

**[CORRECTION]** A three-way self-join comparing three different type values proves three product *types*, not three different PC models. For the latter, GROUP BY maker with COUNT(DISTINCT model) is the direct answer.

---

# 6. Subqueries

## 6.1 Scalar, row, table, and correlated subqueries

- **Scalar subquery:** returns one value.
- **Row subquery:** returns one row with one or more columns.
- **Table subquery:** returns a relation.
- **Correlated subquery:** refers to a row of the outer query and is logically reevaluated for each outer row, although an optimizer may transform it.

Highest-paid employee:

~~~sql
SELECT id
FROM Employee
WHERE salary = (SELECT MAX(salary) FROM Employee);
~~~

This returns all ties. A hard-coded maximum does not generalize.

## 6.2 ALL and ANY/SOME

For a nonempty set S:

- x >= ALL(S): x is at least the maximum.
- x <= ALL(S): x is at most the minimum.
- x > ANY(S): x exceeds at least one member.
- x < ANY(S): x is below at least one member.
- ANY and SOME are synonyms in standard SQL.

~~~sql
SELECT id
FROM Employee
WHERE salary >= ALL (SELECT salary FROM Employee);
~~~

**Empty-set edge case:** comparison with ALL(empty) is TRUE; comparison with ANY(empty) is FALSE. NULLs can introduce UNKNOWN.

## 6.3 Correlated average

Employees earning above their own department's average:

~~~sql
SELECT e.*
FROM Employee e
WHERE e.salary > (
    SELECT AVG(x.salary)
    FROM Employee x
    WHERE x.dept = e.dept
);
~~~

The inner x.dept = e.dept is the correlation.

## 6.4 Highest per group

Row-value form from the slides:

~~~sql
SELECT id, dept, salary
FROM Employee
WHERE (dept, salary) IN (
    SELECT dept, MAX(salary)
    FROM Employee
    GROUP BY dept
);
~~~

Join form:

~~~sql
SELECT e.*
FROM Employee e
JOIN (
    SELECT dept, MAX(salary) AS max_salary
    FROM Employee
    GROUP BY dept
) m
  ON m.dept = e.dept
 AND m.max_salary = e.salary;
~~~

Both preserve ties.

## 6.5 EXISTS and NOT EXISTS

EXISTS is TRUE if its subquery produces at least one row. The selected expression is irrelevant; SELECT 1 is conventional.

~~~sql
-- Makers that sell both
SELECT DISTINCT p.maker
FROM PC p
WHERE EXISTS (
    SELECT 1
    FROM Laptop l
    WHERE l.maker = p.maker
);

-- Makers of PCs but no laptops
SELECT DISTINCT p.maker
FROM PC p
WHERE NOT EXISTS (
    SELECT 1
    FROM Laptop l
    WHERE l.maker = p.maker
);
~~~

## 6.6 Derived tables in FROM

Makers of at least two computers—PC or laptop—with speed at least 2:

~~~sql
SELECT maker
FROM (
    SELECT p.maker, pc.model
    FROM Product p
    JOIN PC pc ON pc.model = p.model
    WHERE pc.speed >= 2

    UNION

    SELECT p.maker, l.model
    FROM Product p
    JOIN Laptop l ON l.model = p.model
    WHERE l.speed >= 2
) fast_computer
GROUP BY maker
HAVING COUNT(*) >= 2;
~~~

UNION removes a duplicate model/maker pair. UNION ALL would be safe only if model identifiers are known disjoint or COUNT(DISTINCT model) is used.

## 6.7 Subquery viva traps

- Scalar subquery returning more than one row causes an error.
- = expects one value; IN accepts a set.
- Correlation must use aliases correctly.
- NOT IN is dangerous when the subquery can yield NULL; NOT EXISTS is safer.
- EXISTS can stop after the first match.
- A CTE (WITH clause) improves naming/readability but is not automatically materialized.

---

# 7. Data Modification

## 7.1 INSERT

~~~sql
INSERT INTO Student (id, first_name, last_name)
VALUES ('S987654321', 'Jane', 'Smith');

INSERT INTO Laptop (model, speed, ram, hd, screen, price)
SELECT model + 1100, speed, ram, hd, 17, price + 500
FROM PC;
~~~

Omitted nullable/defaulted columns receive their default or NULL. Always list columns in production code so schema order changes do not silently corrupt meaning.

## 7.2 Bulk insert versus CTAS

~~~sql
INSERT INTO ExistingTable (a, b)
SELECT x, y
FROM SourceTable;

CREATE TABLE NewTable AS
SELECT x, y
FROM SourceTable;
~~~

The first adds rows to an existing schema. The second creates a table from query output and has the CTAS metadata limitation described earlier.

## 7.3 DELETE and referential order

~~~sql
DELETE FROM Product
WHERE model IN (SELECT model FROM PC WHERE hd < 100);

DELETE FROM PC
WHERE hd < 100;
~~~

If Product has a foreign key to PC, the legal order may instead require deleting the child first, using ON DELETE CASCADE, or deferring constraints. Never infer deletion order without checking relationships.

## 7.4 UPDATE

~~~sql
UPDATE Product
SET maker = 'A'
WHERE maker = 'B';

UPDATE Laptop
SET screen = screen + 1,
    price  = price - 100
WHERE model IN (
    SELECT p.model
    FROM Product p
    WHERE p.type = 'laptop'
      AND p.maker = 'B'
);
~~~

An UPDATE without WHERE affects every row.

## 7.5 Transaction safety for DML

For an important modification:

1. preview the predicate with SELECT;
2. start a transaction or disable autocommit;
3. perform DML;
4. verify row count and invariants;
5. COMMIT if correct, otherwise ROLLBACK.

---

# 8. Integrity Constraints

## 8.1 Why constraints belong in the database

**[SLIDE]** Applications can contain bugs and several applications may write the same database. A database constraint creates a central invariant checked on every relevant modification.

Main classes:

- domain/type constraints;
- NOT NULL;
- PRIMARY KEY / UNIQUE;
- FOREIGN KEY referential integrity;
- CHECK;
- assertions in the SQL standard;
- triggers for procedural rules.

## 8.2 Foreign keys

~~~sql
CREATE TABLE Employee (
    id      INTEGER PRIMARY KEY,
    name    VARCHAR2(50),
    address VARCHAR2(100),
    gender  CHAR(1)
);

CREATE TABLE Department (
    name VARCHAR2(10) PRIMARY KEY,
    head INTEGER,
    CONSTRAINT department_head_fk
        FOREIGN KEY (head)
        REFERENCES Employee(id)
        ON DELETE SET NULL
);
~~~

The referenced columns must be a candidate key (PRIMARY KEY or UNIQUE).

Effects:

- Insert/update a child FK: allowed if NULL is permitted or the referenced key exists.
- Delete a child row: does not threaten the parent reference.
- Insert a parent: ordinarily does not threaten existing children.
- Update/delete a referenced parent key: rejected under NO ACTION/RESTRICT if children exist, unless an action such as CASCADE or SET NULL applies.

Common actions:

- ON DELETE/UPDATE CASCADE: propagate key deletion/change.
- SET NULL: clear child FK; child column must allow NULL.
- SET DEFAULT: set declared default, where supported.
- RESTRICT/NO ACTION: reject; exact timing differs.

**Oracle note:** Oracle supports ON DELETE CASCADE/SET NULL, but not a general ON UPDATE CASCADE clause. The lecture syntax is conceptual/standard rather than portable Oracle SQL.

## 8.3 CHECK constraints and implication

~~~sql
speed NUMBER(3,2) CHECK (speed >= 2.0)

type VARCHAR2(20)
    CHECK (type IN ('laser', 'ink-jet', 'bubble-jet'))
~~~

Tuple-level check:

“If speed < 2, price must be ≤ 800.”

P → Q is equivalent to ¬P ∨ Q:

~~~sql
CHECK (speed >= 2.0 OR price <= 800)
~~~

“If screen < 15, then hd ≥ 40 or price < 1000”:

~~~sql
CHECK (screen >= 15 OR hd >= 40 OR price < 1000)
~~~

**NULL trap:** a CHECK rejects FALSE but normally accepts TRUE or UNKNOWN. Add NOT NULL when UNKNOWN must not pass.

**[CORRECTION]** Subqueries are not allowed inside CHECK constraints in Oracle and many DBMSs. Cross-table conditions need a suitable FK, trigger, assertion if supported, or application/transaction design.

## 8.4 Assertions

**[SLIDE + PORTABILITY NOTE]** SQL defines database-wide assertions:

~~~sql
CREATE ASSERTION no_pc_and_laptop_maker
CHECK (
    NOT EXISTS (
        SELECT 1
        FROM Product pc
        JOIN Product laptop
          ON laptop.maker = pc.maker
        WHERE pc.type = 'pc'
          AND laptop.type = 'laptop'
    )
);
~~~

The useful design pattern is:

> Find a violating row; require that no such row exists.

Most commercial DBMSs, including Oracle, do not implement CREATE ASSERTION. Use triggers or redesign where necessary.

## 8.5 Naming and altering constraints

~~~sql
ALTER TABLE Product
ADD CONSTRAINT product_price_nonnegative CHECK (price >= 0);

ALTER TABLE Product
DROP CONSTRAINT product_price_nonnegative;
~~~

Names make diagnostics and schema migration manageable.

## 8.6 Triggers

**[SLIDE, Oracle form]**

~~~sql
CREATE OR REPLACE TRIGGER no_negative_pc
BEFORE INSERT OR UPDATE OF price, speed ON PC
FOR EACH ROW
WHEN (NEW.price < 0 OR NEW.speed < 0)
BEGIN
    RAISE_APPLICATION_ERROR(-20000, 'No negative value allowed');
END;
/
~~~

Inside an Oracle row trigger, values are normally referenced as :NEW.column and :OLD.column in the PL/SQL body.

Cascade example:

~~~sql
CREATE OR REPLACE TRIGGER delete_product_with_pc
BEFORE DELETE ON PC
FOR EACH ROW
BEGIN
    DELETE FROM Product
    WHERE model = :OLD.model;
END;
/
~~~

Prefer a declarative FK with ON DELETE CASCADE when it expresses the rule. Triggers are powerful but can hide side effects, recurse, introduce ordering problems, and complicate bulk operations.

## 8.7 Constraint selection guide

| Rule | Best mechanism |
|---|---|
| value required | NOT NULL |
| one row identifier | PRIMARY KEY |
| alternate identifier | UNIQUE |
| child must reference parent | FOREIGN KEY |
| condition within one row | CHECK |
| derived access subset | VIEW |
| procedural/cross-table rule | trigger, carefully |
| all-or-nothing multi-step invariant | transaction + constraints |

---

# 9. The Supplied Oracle Labs

## 9.1 SQL*Plus and SQL*Loader workflow

**[SLIDE + LAB]**

~~~text
sqlplus username/password @schema_script
sqlldr username/password control=loadFile.ctr log=load.log bad=load.bad
~~~

A SQL*Loader control file specifies:

- input file;
- target table;
- insertion mode such as APPEND;
- delimiter and optional quote;
- destination column order.

Generic slide form:

~~~text
LOAD DATA
INFILE 'data.csv'
APPEND INTO TABLE Target
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
(column1, column2, column3)
~~~

Other SQL*Plus commands in the starter deck:

- @script runs a script.
- SPOOL file captures output.
- PAUSE pauses a script.
- COLUMN ... FORMAT controls display.
- ALTER USER changes a password.
- QUIT exits.

**Security correction:** never expose passwords in command history or scripts, and do not grant DBA to an ordinary application user. The broad GRANT DBA example is suitable only for a tightly controlled teaching setup.

## 9.2 Product database—course teaching schema

**[COURSE EXAMPLE]**

~~~sql
CREATE TABLE PC (
    model NUMBER(4) PRIMARY KEY,
    speed NUMBER(3,2),
    ram   NUMBER(4),
    hd    NUMBER(3),
    price NUMBER(7,2)
);

CREATE TABLE Product (
    maker VARCHAR2(25),
    model NUMBER(4) PRIMARY KEY,
    type  VARCHAR2(7)
);

CREATE TABLE Laptop (
    model  NUMBER(4) PRIMARY KEY,
    speed  NUMBER(3,2),
    ram    NUMBER(4),
    hd     NUMBER(3),
    screen NUMBER(3,1),
    price  NUMBER(7,2)
);

CREATE TABLE Printer (
    model NUMBER(4) PRIMARY KEY,
    color CHAR(1),
    type  VARCHAR2(7),
    price NUMBER(7,2)
);
~~~

Representative rows for tracing queries:

~~~text
PC:      1001,2.66,1024,250,2114
Laptop:  2001,2,2048,240,20.1,3673
Printer: 3001,T,ink-jet,99
Product: A,1001,pc
~~~

Useful test queries count each table and union PC/Laptop makers:

~~~sql
SELECT COUNT(*) AS Product FROM Product;
SELECT COUNT(*) AS PC FROM PC;
SELECT COUNT(*) AS Laptop FROM Laptop;
SELECT COUNT(*) AS Printer FROM Printer;

SELECT p.maker
FROM PC x
JOIN Product p ON p.model = x.model
UNION
SELECT p.maker
FROM Laptop x
JOIN Product p ON p.model = x.model;
~~~

**Schema-design observation:** `Product.model` logically describes the supertype of PC/Laptop/Printer models. If subtype tables have no foreign keys to `Product` and `Product.type` has no `CHECK`, the DBMS cannot enforce that correspondence; a stronger design should enforce those invariants.

## 9.3 Movie database—course teaching schema

**[COURSE EXAMPLE]**

~~~sql
CREATE TABLE Movie (
    title  CHAR(50),
    year   INTEGER,
    length INTEGER,
    genre  CHAR(30),
    studio CHAR(30),
    certno INTEGER,
    PRIMARY KEY (title, year)
);

CREATE TABLE MovieStar (
    name    VARCHAR2(100) PRIMARY KEY,
    birth   DATE,
    wealth  INTEGER,
    address VARCHAR2(50)
);

CREATE TABLE StarsIn (
    title CHAR(50),
    year  INTEGER,
    name  VARCHAR2(100),
    PRIMARY KEY (title, year, name)
);

CREATE TABLE Studio (
    name    CHAR(30) PRIMARY KEY,
    address VARCHAR2(50),
    certno  INTEGER
);

CREATE TABLE MovieExec (
    name    CHAR(30),
    certno  INTEGER,
    address VARCHAR2(100),
    wealth  INTEGER
);
~~~

**Schema-design observations:**

- StarsIn should normally have FKs (title,year) → Movie and name → MovieStar.
- Movie.studio should normally reference Studio.name.
- Movie.certno may represent an executive certificate and should reference a UNIQUE key in MovieExec; if MovieExec has no declared key, that relationship cannot be enforced.
- CHAR fields preserve padding behavior visible in the SQL lectures.

---

# 10. Relational Algebra

## 10.1 Why it matters

**[SLIDE]**

SQL query → relational-algebra expression → logically optimized expression → physical evaluation plan.

Relational algebra is procedural enough to express an operator tree, compositional because every operator returns a relation, and the foundation of logical query optimization.

## 10.2 Basic operators

Let R and S be relations:

- Selection: σ_condition(R)—choose rows.
- Projection: π_attributes(R)—choose columns and remove duplicates in classical RA.
- Cartesian product: R × S.
- Union: R ∪ S.
- Difference: R − S.
- Rename: ρ_newname/list(R).

Derived:

- intersection: R ∩ S = R − (R − S);
- theta join: R ⋈_θ S = σ_θ(R × S);
- equijoin: theta join whose predicate is equality;
- natural join: equality on every common-named attribute, followed by removal of duplicate common columns.

Classical RA uses set semantics; SQL normally uses bags.

## 10.3 Translation examples

SQL:

~~~sql
SELECT DISTINCT s.sname, s.gpa
FROM Students s
WHERE s.gpa > 3.5;
~~~

RA:

π_sname,gpa(σ_gpa>3.5(Students))

SQL:

~~~sql
SELECT DISTINCT s.gpa, p.address
FROM Students s
JOIN People p ON p.sname = s.sname
WHERE s.gpa > 3.5;
~~~

RA:

π_gpa,address(σ_gpa>3.5(Students) ⋈_Students.sname=People.sname People)

## 10.4 Self-join requires rename

Find different PCs with the same hard-disk size:

π_p1.hd(
  σ_p1.model≠p2.model ∧ p1.hd=p2.hd(
    ρ_p1(PC) × ρ_p2(PC)
  )
)

To list each pair once, use p1.model < p2.model.

## 10.5 Maximum without aggregation

To find tuples not dominated by a faster tuple:

1. R1(model,speed) = π_model,speed(PC) ∪ π_model,speed(Laptop)
2. Slower = π_R1.model,R1.speed(σ_R1.speed<R2.speed(R1 × ρ_R2(R1)))
3. Fastest = R1 − Slower

This “all candidates minus those with a witness that beats them” pattern is a classic way to express maximum in basic RA.

## 10.6 Operator precedence from the deck

Highest to lowest:

1. selection σ, projection π, rename ρ;
2. Cartesian product and join;
3. intersection;
4. union and difference.

Parenthesize in a viva answer rather than relying on precedence.

## 10.7 Logical optimization rules

Safe transformations include:

- split conjunctive selections:
  σ_(p∧q)(R) ≡ σ_p(σ_q(R));
- commute selections:
  σ_p(σ_q(R)) ≡ σ_q(σ_p(R));
- combine product + predicate:
  σ_θ(R×S) ≡ R⋈_θS;
- inner/natural joins commute and associate;
- push a selection below a join when its attributes come from only one input;
- push projections down while retaining output and join attributes;
- eliminate redundant nested projections.

Why push selections/projections down? It reduces the number and width of intermediate tuples, usually reducing I/O, memory, and CPU.

Outer joins require special care: pushing a predicate to the nullable side can change NULL-extended rows and therefore change semantics.

## 10.8 Relational calculus

**[CORE SUPPLEMENT—no detailed calculus deck was supplied]**

Relational calculus is declarative: specify properties of the desired tuples.

- **Tuple relational calculus (TRC):** variables range over tuples.
- **Domain relational calculus (DRC):** variables range over attribute values.

TRC example, names of students with GPA > 3.5:

{ t.sname | Students(t) ∧ t.gpa > 3.5 }

Calculus expressions must be **safe/range-restricted** so the answer is finite and based on the active database domain. Relational algebra and safe relational calculus have equivalent expressive power—Codd's theorem.

---

# 11. ER and EER Modeling

## 11.1 Design process

**[SLIDE]**

1. **Requirements analysis:** what data, operations, users, and constraints exist?
2. **Conceptual design:** precise but stakeholder-readable ER/EER model.
3. **Logical design:** translate it to relations, keys, and constraints.
4. **Physical design:** files, indexes, partitions, placement.
5. **Security design:** authorization and protection.

This process is iterative.

Store birth date rather than age because age is time-dependent and derivable. This avoids continual updates and inconsistency.

## 11.2 Entity, entity set, attribute, relationship

- **Entity:** distinguishable real-world object.
- **Entity set:** similar entities; drawn as a rectangle.
- **Attribute:** property; drawn as an oval in the supplied Chen notation.
- **Relationship:** association among entities; drawn as a diamond.
- **Relationship set:** set of relationship instances.

Entities often come from nouns; relationships often come from verbs, but grammar is only a discovery aid, not a design rule.

Mathematically, a binary relationship R between entity sets A and B is a subset of A × B. An n-ary relationship is a subset of E1 × ... × En.

## 11.3 Attributes

Common classifications:

- simple versus composite;
- single-valued versus multivalued;
- stored versus derived;
- key versus non-key;
- optional versus mandatory.

**[SLIDE design rule]** If multiple structured addresses must be stored, Address is often better modeled as an entity than as repeated attributes Addr1, Addr2. Make something an entity when it has identity, structure, multiple values, its own relationships, or independent lifecycle.

## 11.4 Cardinality and participation

Maximum cardinality:

- 1:1—each side relates to at most one on the other side.
- 1:N—one X may relate to many Y; each Y to at most one X.
- M:N—many on both sides.

Minimum participation:

- **partial/optional:** an entity may participate zero times.
- **total/mandatory:** every entity must participate at least once.

The deck uses arrows for “at most one” and a rounded/total form for “exactly one.” Other notations use crow's feet and (min,max), so explain the semantics instead of relying only on symbols.

Degree constraints can express limits such as “a movie has at most 10 actors.”

## 11.5 Relationship attributes

An attribute belongs on a relationship when it depends on the combination:

- salary of an Actor for a particular Film;
- date on which a Person purchased a Product;
- signing money for a particular Actor–Film–Studio contract.

It does not belong solely to Actor or Film because it can change with the pairing.

## 11.6 Recursive relationships

Employee manages Employee uses role names:

- manager role;
- worker/subordinate role.

Possible mapping:

~~~text
Employee(id PK, name, address, manager_id FK -> Employee.id)
~~~

This works for one manager per worker. For M:N mentorship, use a separate relation such as Mentors(mentor_id, mentee_id, ...).

## 11.7 Ternary relationships

Actor–Film–Studio Contract means the fact depends on all three participants. Replacing it with three independent binary relationships may create combinations that never formed one contract.

Mapping:

~~~text
Contract(actor_id FK, film_id FK, studio_id FK, salary,
         PK(actor_id, film_id, studio_id))
~~~

If a given Actor–Film pair determines exactly one Studio, then (actor_id, film_id) can be the key and studio_id is functionally determined.

## 11.8 ER-to-relational mapping algorithm

### Strong entity

Create one relation containing simple attributes. Choose its key as PK. Decompose composite attributes; derived attributes are often omitted.

### Multivalued attribute

Create a separate relation:

~~~text
PersonPhone(person_id FK, phone_number,
            PK(person_id, phone_number))
~~~

### M:N relationship

Create a bridge relation with participating keys as FKs, normally forming a composite PK, plus relationship attributes.

~~~sql
CREATE TABLE Purchased (
    product_name VARCHAR2(50),
    person_id    INTEGER,
    purchase_date DATE,
    PRIMARY KEY (product_name, person_id),
    FOREIGN KEY (product_name) REFERENCES Product(name),
    FOREIGN KEY (person_id) REFERENCES Person(id)
);
~~~

If the same person may buy the same product more than once, date or a purchase_id must join the key. The key must reflect requirements, not a diagram template.

### 1:N relationship

Put the key of the 1-side as an FK on the N-side. Put relationship attributes there too.

Film N:1 Director:

~~~text
Director(id PK, name)
Film(title, year, type, director_id FK, salary,
     PK(title, year))
~~~

If participation is total, mark director_id NOT NULL.

### 1:1 relationship

Put an FK in either relation; prefer:

- the side with total participation, to avoid NULLs;
- the side that naturally depends on the other.

Add UNIQUE to enforce at most one:

~~~text
President(person_id PK/FK, studio_name UNIQUE NOT NULL FK)
~~~

Alternatively make a separate relationship relation if it has substantial attributes or independent meaning.

### Weak entity

A weak entity lacks a full key of its own and is existence-dependent on an identifying owner. Its partial key distinguishes weak entities within one owner.

~~~text
University(name PK, address, total_team)
Team(university_name FK, number partial-key, team_name, coach,
     PK(university_name, number))
~~~

The identifying relationship normally needs no separate table.

## 11.9 Specialization/generalization (ISA)

Product may have overlapping subtypes SoftwareProduct and EducationalProduct. A subtype inherits the supertype's attributes and may add its own.

Important constraints:

- **disjoint** versus **overlapping** subtypes;
- **total** versus **partial** specialization.

Mapping strategies:

1. **One table for hierarchy:** nullable subtype fields and a type discriminator. Simple reads; many NULLs; overlapping types are awkward.
2. **Superclass + subtype tables:** Product(key,...), SoftwareProduct(key PK/FK,...), EducationalProduct(key PK/FK,...). Flexible and faithful; joins reconstruct full subtype.
3. **Concrete-subclass tables:** duplicate inherited columns in each subtype; works best for total, disjoint specialization but duplicates schema/data.

The supplied deck chooses superclass + subtype tables and emphasizes that an ER entity may belong to overlapping subtype entity sets.

## 11.10 Good-design tests from the slides

- Be faithful to the real constraint.
- Do not model the same fact twice, such as both Movie.studioName and a separate OwnedBy relation.
- Do not turn every value into an entity; use the right kind of element.
- Do not invent entities merely to make the picture elaborate.
- Do not replace a meaningful n-ary fact with binary facts that lose its semantics.
- Ask what uniquely identifies every entity and relationship instance.

## 11.11 Whiteboard modeling checklist

1. Underline nouns/entities and verbs/relationships.
2. Identify candidate keys.
3. Attach attributes to the fact that determines them.
4. State min/max participation in words.
5. Check recursive roles and n-ary facts.
6. Identify weak entities and partial keys.
7. State subtype disjointness/completeness.
8. Map to tables.
9. Add PK, UNIQUE, FK, NOT NULL, CHECK.
10. Test insert, update, delete, and duplicate scenarios.

---

# 12. Functional Dependencies and Normalization

## 12.1 Why normalize?

Poor design produces:

- **redundancy:** the same fact repeats;
- **update anomaly:** one fact must be changed in several rows;
- **insertion anomaly:** cannot record one fact without another;
- **deletion anomaly:** deleting one fact unintentionally removes another.

Example:

PersonPhoneCity(name, ssn, phone, city)

If ssn → name, city and a person has many phones, name and city repeat. Deleting the final phone can erase knowledge of the person's city.

Decompose:

~~~text
Person(ssn, name, city)
Phone(ssn, phone)
~~~

## 12.2 Functional dependency

For relation R, X → Y holds if every pair of legal tuples agreeing on X must also agree on Y.

Formally:

∀t1,t2 ∈ R: t1[X] = t2[X] ⇒ t1[Y] = t2[Y].

An FD is a semantic constraint over **all legal instances**, not a pattern guessed from one sample.

Movie example:

(title, year) → length, genre, studio

but normally not:

(title, year) → starName

because one movie can have multiple stars.

## 12.3 Trivial and nontrivial FDs

- X → Y is **trivial** if Y ⊆ X.
- **Nontrivial** if some attribute of Y is outside X.
- **Completely nontrivial** if X ∩ Y = ∅.

## 12.4 Armstrong's axioms and derived rules

The sound and complete axioms:

1. **Reflexivity:** if Y ⊆ X, then X → Y.
2. **Augmentation:** if X → Y, then XZ → YZ.
3. **Transitivity:** if X → Y and Y → Z, then X → Z.

Derived:

- union: X→Y and X→Z imply X→YZ;
- decomposition: X→YZ implies X→Y and X→Z;
- pseudotransitivity: X→Y and WY→Z imply WX→Z.

The lecture calls union/decomposition “combining/splitting” and demonstrates closure as the easier systematic method.

## 12.5 Attribute closure algorithm

Given F and attribute set X, X+ is every attribute functionally determined by X.

~~~text
closure(X, F):
    result := X
    repeat
        changed := false
        for each FD A -> B in F:
            if A subset-of result and B not subset-of result:
                result := result union B
                changed := true
    until not changed
    return result
~~~

With singleton right sides, a direct implementation is O(|F||R|) per pass and at most |R| useful additions, so a simple bound is O(|F||R|²); optimized implementations do better. In a viva, the invariant matters more: result always contains exactly attributes already proved to depend on X.

### Worked slide example

R(name, category, color, department, price)

F:

- name → color
- category → department
- color, category → price

Compute {name, category}+:

1. start {name, category};
2. name → color: add color;
3. category → department: add department;
4. color,category → price: add price.

Closure is all attributes, so {name,category} is a superkey. Neither singleton closure is all attributes, so it is a candidate key.

### Another slide example

R(A,B,C,D,E,F), F = {AB→C, AD→E, B→D, AF→B}.

- (AB)+ = {A,B,C,D,E}; it lacks F.
- (AF)+ starts {A,F}; AF→B, B→D, AB→C, AD→E, so (AF)+ = all attributes. AF is a superkey and, since neither A nor F alone closes to all, a key.

## 12.6 Uses of closure

- Test whether X → A follows from F: compute X+; check A ∈ X+.
- Test superkey: X+ = all attributes.
- Test candidate key: X is superkey and no proper subset is.
- Detect BCNF violations.
- Test extraneous attributes and redundant FDs.

## 12.7 Finding candidate keys efficiently

Useful rules:

1. Any attribute never appearing on any RHS cannot be derived; it must be in every key.
2. Attributes only on RHS are usually not needed as starting attributes.
3. Start with mandatory attributes, compute closure, and add combinations of remaining attributes.
4. Once a superkey is found, do not examine its supersets as candidate keys.
5. Verify minimality by removing each attribute.

**[SLIDE counting examples]** If R has n attributes:

- only key {A1}: 2^(n−1) superkeys;
- only singleton keys {A1}, {A2}: 3·2^(n−2), by inclusion–exclusion;
- keys {A1} and {A2,A3}: 5·2^(n−3);
- keys {A1,A2} and {A1,A3}: 3·2^(n−3).

## 12.8 Canonical/minimal cover

**[CORE SUPPLEMENT—the supplied design deck teaches closure and BCNF but not the complete canonical-cover algorithm]**

A canonical cover Fc is equivalent to F but has:

- one attribute on each RHS during calculation;
- no extraneous LHS attribute;
- no redundant FD;
- optionally, FDs with identical LHS combined at the end.

Algorithm:

~~~text
canonical_cover(F):
    1. Split X -> A1A2... into X -> A1, X -> A2, ...
    2. Repeatedly remove extraneous LHS attributes:
           for B in X of X -> A,
           if A is in (X - {B})+ under current F,
           replace X -> A by (X - {B}) -> A
    3. Remove redundant dependencies:
           X -> A is redundant if A is in X+
           under F - {X -> A}
    4. Repeat until stable.
    5. Optionally combine X -> A and X -> B as X -> AB.
~~~

### Worked canonical-cover example

F = {A→BC, B→C, A→B, AB→C}.

1. Split A→BC into A→B and A→C.
2. Remove duplicates.
3. A→C is implied by A→B and B→C, so remove it.
4. In AB→C, A is extraneous because B→C already holds; it becomes B→C, a duplicate.

Canonical cover: {A→B, B→C}.

Do not test redundancy using the FD itself; temporarily remove it.

## 12.9 First normal form

**[SLIDE]** 1NF requires each attribute value to be atomic with respect to the relational schema—no repeating group/list in one cell.

Bad:

~~~text
Student(name, gpa, courses={DB,OS})
~~~

Better:

~~~text
Student(student_id, name, gpa)
Course(course_id, ...)
Takes(student_id, course_id)
~~~

“Atomic” is model-dependent: a string is treated atomically even though it contains characters.

## 12.10 Second normal form

**[SLIDE + CORRECTION]** A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on **every candidate key**—there is no dependency on a proper subset of a candidate key.

2NF matters only when a candidate key is composite.

Example:

Enrollment(student_id, course_id, student_name, course_title, grade)

Key: (student_id, course_id)

- student_id → student_name: partial dependency.
- course_id → course_title: partial dependency.

Decompose Student, Course, Enrollment.

The slide calls 2NF “obsolete” in the sense that stronger normal forms are usually the real design target; the definition remains valid.

## 12.11 Third normal form

**[CORE SUPPLEMENT—the slide directs the reader to the book]**

R is in 3NF if for every nontrivial FD X → A in F+:

- X is a superkey, **or**
- A is prime.

Mnemonic: every non-key fact should depend on “the key, the whole key, and nothing but the key,” but use the formal definition in a viva.

Example:

Employee(emp_id, dept_id, dept_name)

emp_id → dept_id and dept_id → dept_name. emp_id is key; dept_id is not; dept_name is non-prime. dept_id → dept_name violates 3NF. Decompose Employee(emp_id,dept_id) and Department(dept_id,dept_name).

## 12.12 Boyce–Codd normal form

**[SLIDE]** R is in BCNF if for every nontrivial FD X → Y in F+, X is a superkey.

Equivalent closure test: there must be no X with:

X ≠ X+ ≠ all attributes.

BCNF is stricter than 3NF because it has no “RHS is prime” exception.

Every two-attribute relation is in BCNF:

- with no nontrivial FD, none violates;
- if A→B, A is a key;
- if B→A, B is a key;
- if both, both are keys.

## 12.13 BCNF decomposition

Given a violating FD X → Y in R:

~~~text
R1 := X union Y
R2 := R - (Y - X)
    = X union (R - Y)
recursively decompose R1 and R2
~~~

Slide closure form:

~~~text
find X such that X != X+ != R
Y := X+ - X
Z := R - X+
decompose into R1(X union Y), R2(X union Z)
~~~

### Worked slide example

R(A,B,C,D), F = {A→B, B→C}.

A+ = ABC, so A is not a superkey and A→B violates BCNF.

- Decompose R into R1(A,B,C) and R2(A,D).
- In R1, B+ = BC, so B→C violates.
- Decompose R1 into R11(B,C) and R12(A,B).

Final BCNF relations: BC, AB, AD.

### Person example

Person(name, ssn, age, hairColor, phone)

FDs: ssn→name,age and age→hairColor.

1. ssn+ includes name, age, hairColor but not phone:
   - P(ssn,name,age,hairColor)
   - Phone(ssn,phone)
2. age→hairColor violates BCNF inside P:
   - People(ssn,name,age)
   - Hair(age,hairColor)

All are lossless under the decomposing FDs.

## 12.14 Lossless join and dependency preservation

**[CORE SUPPLEMENT]**

Two properties are different:

- **Lossless join:** joining decomposed relations recreates exactly the legal original relation—no missing or spurious tuples.
- **Dependency preservation:** every original FD can be enforced by checking individual decomposed relations without joining them.

For binary decomposition R → R1,R2, it is lossless with respect to F iff:

(R1 ∩ R2) → R1

or:

(R1 ∩ R2) → R2

is in F+.

BCNF decomposition is lossless but may lose dependency preservation. 3NF synthesis can guarantee both losslessness and dependency preservation.

## 12.15 3NF synthesis algorithm

**[CORE SUPPLEMENT]**

~~~text
1. Compute a canonical cover Fc.
2. For each FD X -> A in Fc, create relation XA.
   Combine FDs with the same X when convenient.
3. If no created relation contains a candidate key of R,
   add one relation containing a candidate key.
4. Remove any relation schema contained entirely in another.
~~~

This gives a dependency-preserving, lossless 3NF decomposition.

## 12.16 3NF versus BCNF

| Property | 3NF | BCNF |
|---|---|---|
| Determinant rule | superkey or RHS prime | determinant must be superkey |
| Removes most anomalies | yes | stronger |
| Lossless decomposition available | yes | yes |
| Dependency preservation always achievable | yes via synthesis | not always |

Choose BCNF when dependencies can still be conveniently enforced; choose 3NF when preserving all dependencies is essential.

## 12.17 4NF and 5NF

**[CORE SUPPLEMENT, compact]**

- A multivalued dependency X ↠ Y says that for each X, Y values vary independently of the remaining attributes.
- R is in **4NF** if every nontrivial MVD X ↠ Y has X as a superkey.
- **5NF/project-join NF** removes redundancy caused only by join dependencies not implied by keys.

For most undergraduate vivas: explain 1NF, 2NF, 3NF, BCNF deeply; mention 4NF for independent multivalued facts and 5NF for rare join dependencies.

## 12.18 Normalization whiteboard routine

1. Write R and F.
2. Split RHSs.
3. Compute candidate keys with closure.
4. Mark prime attributes.
5. Test 2NF, then 3NF, then BCNF using formal conditions.
6. Pick a violating FD and decompose.
7. Project relevant FDs onto each new relation.
8. Repeat.
9. Prove losslessness.
10. Check dependency preservation.

---

# 13. Physical Storage Systems

## 13.1 The storage hierarchy

**[SLIDE]** A DBMS places data across a hierarchy because no single medium is simultaneously fastest, largest, cheapest, and most durable.

| Level | Typical examples | Volatile? | DBMS role |
|---|---|---:|---|
| CPU registers/cache | SRAM-backed processor cache | yes | instructions and immediately used values |
| Main memory | DRAM | yes | buffer pool, hash tables, sorting, lock table |
| Secondary/on-line storage | SSD, magnetic disk | no | active database, indexes, log |
| Tertiary/off-line storage | tape, optical/archive | no | backup and archival data |

- **Volatile storage** loses contents when power disappears.
- **Nonvolatile storage** retains contents without ordinary power.
- **Stable storage** is an abstraction: data survives the failures under the assumed failure model, usually through redundancy plus careful write and recovery protocols. No physical device is literally infallible.
- A **block/page** is the usual unit of allocation and transfer between storage and memory. The deck gives a typical disk-block range of 4–16 KiB; real DBMS page sizes are configurable or implementation-specific.
- Smaller pages may increase transfers and metadata; larger pages may waste space, read irrelevant data, and amplify writes.

**Viva:** Why is a DBMS page larger than a record? Because one I/O has a large fixed latency, so transferring several nearby records per I/O exploits spatial locality and amortizes that latency.

## 13.2 DAS, SAN, and NAS

**[SLIDE]**

- **Direct-attached storage (DAS):** block device attached directly to one host.
- **Storage-area network (SAN):** a high-speed network gives servers block-level access to shared storage.
- **Network-attached storage (NAS):** exposes a network file-system interface rather than raw block devices.
- SATA, SAS, and NVMe are interface/protocol families. NVMe is designed for low-latency, highly parallel access over PCIe.

The transfer-rate numbers in the supplied deck describe its hardware generation; memorize the architectural differences, not those numbers as permanent limits.

## 13.3 Magnetic-disk anatomy and access time

**[SLIDE]** A hard disk has rotating **platters**, surfaces, concentric **tracks**, track **sectors**, a read/write head per surface, and an arm assembly. Tracks at the same radius form a **cylinder**.

For a random read, the useful model is:

$$
T_{access} \approx T_{seek}+T_{rotational\ latency}+T_{transfer}+T_{controller/queue}.
$$

If rotation speed is $r$ revolutions/second, average rotational latency is approximately:

$$
T_{rotation,avg}=\frac{1}{2r}.
$$

Example: at 7200 RPM, $r=120$ revolutions/s, so average rotational latency is $1/(240)$ s, about 4.17 ms. The deck emphasizes that random I/O wastes time on seeks and rotation, while a long sequential transfer pays that setup cost roughly once.

- **Seek time:** move the arm to the target track.
- **Rotational latency:** wait for the desired sector to rotate under the head.
- **Transfer time:** actually move the bits.
- **IOPS:** random I/O operations supported per second; latency normally dominates small random HDD accesses.
- **Throughput/bandwidth:** bytes transferred per second; especially relevant to large sequential scans.
- **MTTF:** expected continuous operating time before failure under a model. It is not a warranty and does not imply a disk will run that long.

If independent identical disks each have MTTF $M$, a crude approximation for the time until *some* disk among $N$ fails is $M/N$. This explains why a large array needs redundancy even when each individual disk looks reliable.

## 13.4 Flash and SSD behavior

**[SLIDE]** NAND flash is read and programmed in pages but erased in much larger **erase blocks**. A page cannot simply be overwritten in place; its containing erase block eventually must be erased.

Key terms:

- **Flash translation layer (FTL):** maps logical page addresses to physical flash pages.
- **Out-of-place update/remapping:** write a new physical page and change the mapping rather than wait to erase the old page.
- **Garbage collection:** move still-live pages, erase a block, and make it reusable.
- **Wear leveling:** distribute erases so a small set of blocks does not wear out early.
- **Write amplification:** physical bytes written exceed logical bytes requested because of relocation, metadata, and garbage collection.
- **Queue depth:** number of outstanding I/O requests; SSD parallelism can make throughput much higher at a larger queue depth.

The deck contrasts NAND with NOR, introduces storage-class memory, and notes that SSDs remove mechanical seek/rotation but still have device/controller latency, erase constraints, finite endurance, and asymmetric read/write behavior.

**Viva:** Why can an LSM tree suit flash? It converts many small random updates into batched sequential writes and compactions, reducing random page rewrites, although compaction itself can cause write amplification.

## 13.5 RAID: redundancy and parallelism

**[SLIDE]** RAID means **Redundant Array of Independent Disks**. Striping improves parallelism; redundancy improves availability and recoverability from disk failure. RAID is not a backup: it does not by itself protect against accidental deletion, malicious changes, application bugs, or site loss.

For $N$ equal disks of capacity $C$:

| Level | Layout | Usable capacity | Tolerates | Important consequence |
|---|---|---:|---:|---|
| RAID 0 | block striping only | $NC$ | 0 failures | fast, no redundancy |
| RAID 1 | mirroring | roughly $NC/2$ | normally one disk per mirror pair | two copies; good small-write behavior |
| RAID 4 | block striping + dedicated parity | $(N-1)C$ | 1 disk | parity disk becomes a write bottleneck |
| RAID 5 | distributed single parity | $(N-1)C$ | 1 disk | removes dedicated parity bottleneck |
| RAID 6 | distributed dual parity/P+Q | $(N-2)C$ | 2 disks | safer rebuild window, more parity cost |

Parity for corresponding blocks is based on XOR:

$$
P=D_1\oplus D_2\oplus\cdots\oplus D_k.
$$

If $D_j$ is lost, reconstruct it as the XOR of $P$ and all remaining data blocks. A small RAID-5 update commonly performs **read old data + read old parity + write new data + write new parity**, called the small-write penalty. A full-stripe write can compute parity from the new data without reading the old stripe.

The deck's selection rule is useful:

- RAID 1: attractive for many small random writes and database log storage.
- RAID 5: capacity-efficient for large, mostly sequential workloads but only one-disk fault tolerance.
- RAID 6: stronger protection when arrays and rebuild times are large.

Other reliability terms from the deck:

- **Latent sector failure:** previously written data later becomes unreadable.
- **Data scrubbing:** periodically read and validate data, repairing it from mirror/parity.
- **Hot swapping:** replace a failed disk without shutting down.
- **Hot spare:** idle disk available for immediate rebuild.
- **Nonvolatile write cache:** records pending writes across power failure; it must itself be protected.

Independent-failure calculations can exaggerate reliability because correlated failures, controller faults, firmware bugs, fire, and operator mistakes violate the independence assumption.

## 13.6 Optimizing disk-block access

**[SLIDE]**

- **Buffering:** keep likely reused pages in memory.
- **Read-ahead/prefetch:** fetch nearby blocks before they are explicitly requested.
- **Extent allocation:** allocate a run of contiguous blocks rather than isolated blocks.
- **Disk scheduling/elevator (SCAN):** service requests while the arm moves in one direction, then reverse, reducing movement compared with arbitrary order.
- **Defragmentation:** restore physical locality when a file's extents become scattered; much less central to SSD seek cost.

Do not confuse the OS disk scheduler with the DBMS query scheduler or transaction scheduler.

---

# 14. Data Storage Structures and the Buffer Manager

## 14.1 Files, pages, records, and fields

**[SLIDE]** A database is physically stored as files; a file contains pages/blocks; pages contain records; records contain fields. A **record identifier (RID)** is commonly modeled as `(page-id, slot-id)`.

For a fixed record size $n$, record $i$ could begin at byte $n(i-1)$, but allowing a record to cross page boundaries complicates I/O. Systems normally keep an ordinary record within one page or give large fields special storage.

Deletion choices shown in the deck:

1. shift every later record;
2. move the last record into the hole;
3. leave a hole and maintain a free list.

The first two can invalidate physical pointers. Slot indirection is therefore important.

## 14.2 Variable-length records

**[SLIDE]** Variable size arises from `VARCHAR`, nullable attributes, repeating/complex fields, or mixed record types. A common record layout stores:

- fixed-width fields directly;
- each variable-width field as an `(offset, length)` pair;
- variable data in a trailing area;
- a **NULL bitmap** indicating which attributes are NULL.

An offset is preferable to a raw pointer because the record may move within the page.

Large objects such as BLOB/CLOB values may be kept out-of-line, with a locator in the ordinary row. The deck names Oracle's internal/external LOB support and PostgreSQL TOAST as examples.

## 14.3 Slotted pages

**[SLIDE]** A slotted-page header stores:

- the number of slots;
- the boundary of free space;
- for each slot, the record's offset and size.

The slot directory grows from one end and record data from the other:

~~~text
+---------------- page ----------------+
| header | slot directory ->            |
|                                      |
|              free space              |
|                                      |
|            <- record bytes           |
+--------------------------------------+
RID = (page id, stable slot number)
~~~

Compaction can move record bytes inside a page and update only the slot entry; external RIDs remain stable. A deleted slot can be reused, though systems use generation/version protection where stale references are a concern.

## 14.4 File organizations

**[SLIDE]**

| Organization | Strength | Weakness |
|---|---|---|
| Heap | fast insert into any free page; simple | equality/range search scans without an index |
| Sequential/sorted | excellent ordered/range scan | insert may need overflow pages; periodic reorganization |
| Hash file | fast expected equality lookup | poor range/order support; overflow/skew |
| B+ tree file | dynamic ordered access | tree-maintenance and space overhead |
| Multitable clustering | colocates rows frequently joined | poor for scans of only one relation; variable layout |

A heap file uses a **free-space map** to locate pages with sufficient space. A hierarchical free-space map summarizes groups of pages, so insertion does not scan the whole file.

In a sequential file, insertion finds the sorted position; when the target page is full, an overflow record/page is linked. Too many overflow chains destroy locality, motivating reorganization or B+ tree organization.

**Multitable clustering example:** place a department record near its instructor records. `department JOIN instructor` and “one department with its instructors” become cheap; scanning all departments alone now reads unrelated instructor bytes.

## 14.5 Partitioning

**[SLIDE]** Horizontal table partitioning stores subsets separately, for example `Transaction_2024`, `Transaction_2025`, and `Transaction_2026` behind one logical table.

- **Range partition:** year or ordered interval.
- **Hash partition:** hash(key) chooses a partition; balances equality workloads.
- **List partition:** explicit categories/regions.
- **Composite partition:** for example range then hash.

The key optimizer benefit is **partition pruning**: a predicate such as `year = 2026` avoids unrelated partitions. Partitioning can also simplify retention, maintenance, parallelism, and placement on different media. It is not normalization: partitions usually share one logical schema, whereas normalization decomposes attributes/relationships to remove dependency-based redundancy.

## 14.6 System catalog/data dictionary

**[SLIDE]** The DBMS stores metadata as data, including schemas, columns, types, constraints, views, users, privileges, file locations, indexes, and optimizer statistics. The optimizer reads row counts, page counts, distinct-value counts, histograms, and index metadata from this catalog.

**Viva:** Why can stale statistics make a correct query slow? SQL semantics remain correct, but estimated selectivities and intermediate sizes become wrong, so the optimizer may choose a bad join order or access path.

## 14.7 Buffer manager

**[SLIDE]** The **buffer pool** is memory holding copies of database pages. The buffer manager maps page IDs to frames and mediates disk transfer.

On `fix/page request`:

~~~text
if page is already resident:
    increase pin count
    return its frame
else:
    choose an unpinned victim frame
    if victim is dirty: write it safely
    read requested page into the frame
    update page table; set pin count
    return frame
~~~

- **Pin/fix:** prevent eviction while an operator is using a page.
- **Unpin/unfix:** release that protection.
- **Pin count:** multiple users may pin the same page; only count 0 is evictable.
- **Dirty bit:** in-memory page differs from persistent copy and eventually needs writing.
- **Page latch:** short physical-structure mutual exclusion while inspecting/reorganizing a page. It is not the same as a transaction lock held for logical isolation.
- **Forced output:** explicitly push a page to persistent storage when recovery protocol requires it.

## 14.8 Replacement policies

**[SLIDE]** LRU evicts the least recently used unpinned page, but a one-time sequential scan can pollute the pool. DBMSs exploit query knowledge:

- **Toss immediate:** free a page after its last tuple is consumed.
- **MRU in a looping plan:** keep older inner-relation pages likely to be revisited and evict the just-finished page.
- Pin catalog/root-index pages that are accessed frequently.
- Modern systems often use CLOCK/second-chance or scan-resistant variants because exact LRU bookkeeping is expensive.

**[CORRECTION]** “Pinned” means not eligible for eviction; it does not mean not eligible to be written. A dirty pinned page may be flushed, but its frame cannot be reused while pinned.

## 14.9 Row stores versus column stores

**[SLIDE]**

- **Row-oriented:** all attributes of a tuple are colocated. Good for OLTP inserts/updates and fetching a whole entity.
- **Column-oriented:** values of each attribute are stored together. Good for analytical scans that touch few columns, compression, vectorized execution, and cache locality.

Column storage pays for tuple reconstruction and makes point updates/deletes more involved. ORC and Parquet are named in the deck as columnar file formats; hybrid systems may keep both row and column representations.

Example: `SUM(salary)` over 100 million wide employee rows needs only the salary column in a column store, but an OLTP lookup that returns every field of one employee naturally fits row storage.

---

# 15. Indexing

## 15.1 What an index is—and what a search key is not

**[SLIDE]** An index is a smaller access structure whose entries associate **search-key values** with record/page pointers. A search key may be non-unique and need not be a candidate or primary key.

Evaluate an index by:

- access types: equality, range, prefix/order, spatial;
- lookup latency and I/O;
- insertion/deletion/update cost;
- storage overhead;
- clustering and selectivity;
- concurrency/recovery complexity.

Every extra index can speed some reads but makes writes more expensive because the base row and affected indexes must remain consistent.

## 15.2 Ordered, clustering, secondary, dense, and sparse

**[SLIDE]**

- **Clustering index:** its search-key order determines the physical sequential order of the file. The deck also calls it a primary index, but that use of *primary* does **not** imply the search key is the SQL primary key.
- **Secondary/nonclustering index:** order differs from the data-file order.
- **Dense index:** one entry for every search-key value/record-pointer group.
- **Sparse index:** entries for only some values, commonly the first key of each data page; it requires the underlying data to be ordered on that key.

A secondary index normally must be dense at its lowest level because matching records are not discoverable by scanning the next physical block. For a non-unique key, an entry can point to a bucket/list of RIDs.

Why clustering matters: retrieving 10,000 qualifying rows via a clustered index can become a few sequential page reads; a nonclustered index may cause thousands of random base-table page reads. When a predicate matches a large fraction of the table, a sequential scan can beat an index.

## 15.3 Multilevel indexing

**[SLIDE]** If a disk-resident index itself is large, build a sparse outer index on its pages. Repeating this idea creates a shallow hierarchy. B+ trees make this hierarchy dynamic under insertion and deletion.

## 15.4 B+ tree invariants

**[SLIDE]** For a B+ tree whose maximum internal fan-out is $n$:

- search keys inside a node are sorted;
- every root-to-leaf path has the same length;
- an ordinary internal node has between $\lceil n/2\rceil$ and $n$ children;
- an ordinary leaf has between $\lceil(n-1)/2\rceil$ and $n-1$ search-key entries;
- a nonleaf root has at least two children; a root that is also a leaf may be less full;
- internal nodes guide search; all record entries occur at leaves;
- leaves are linked in search-key order, making range scans efficient.

For $K$ search-key values, the deck bounds height by roughly:

$$
h\le \left\lceil\log_{\lceil n/2\rceil}K\right\rceil.
$$

With fan-out near 100 and one million keys, about four root-to-leaf page accesses suffice. Large fan-out—not binary branching—is why database trees stay shallow.

### Search and range search

~~~text
find(key):
    node = root
    while node is internal:
        choose pointer Pi whose separator interval contains key
        node = read(Pi)
    search leaf for key
    return its RID(s), or NOT_FOUND

range(low, high):
    leaf = leaf_found_by_find(low)
    while leaf exists:
        emit entries low <= key <= high
        stop once key > high
        leaf = leaf.next
~~~

The internal separator convention differs among implementations; state the invariant rather than memorizing whether equality follows a left or right pointer in one diagram.

### Insertion

~~~text
insert(key, rid):
    descend to target leaf L
    insert (key, rid) in sorted order
    if L fits: finish
    split L into L and L2; repair leaf-next links
    copy L2's first separator key into parent with pointer to L2
    while parent overflows:
        split the internal node
        push the middle separator upward
    if the old root split:
        create a new root with two child pointers
~~~

Leaf split **copies** a separator into the parent because data entries stay at the leaf. An internal split generally **moves/promotes** the separating key. A root split increases height by exactly one.

### Deletion

~~~text
delete(key, rid):
    descend to leaf L and remove the entry
    repair any parent separator made stale
    if L still meets minimum occupancy: finish
    if a sibling can spare an entry:
        redistribute/borrow and update parent separator
    else:
        merge with a sibling and delete one parent entry
        recursively repair parent underflow
    if root has only one child:
        make that child the new root
~~~

The deck's examples show both repair choices: merge an underfull leaf (deleting Srinivasan) and borrow/redistribute from a sibling (after Singh/Wu). Search, insertion, and deletion require $O(h)=O(\log_n K)$ page visits; constant factors and cache residency matter more than a RAM comparison count.

### Duplicate search keys

Options include:

1. one leaf entry `(key -> RID list/bucket)`;
2. repeated `(key, RID)` entries;
3. make the physical index key `(search_key, primary_key_or_RID)` so it is unique.

Under option 3, equality on `search_key = v` becomes a composite-key range from approximately `(v, -infinity)` to `(v, +infinity)`.

## 15.5 B+ tree versus B-tree

**[SLIDE]** A B-tree may store a record pointer with a key in an internal node, so a successful search can stop early. A B+ tree keeps all data entries at leaves and duplicates separator keys internally.

B+ trees dominate DBMS indexing because:

- internal entries are smaller, increasing fan-out and reducing height;
- every lookup follows a uniform route to a leaf;
- linked leaves make ordered/range scans simple;
- insertion/deletion logic is generally cleaner.

## 15.6 Bulk loading and bottom-up build

**[SLIDE]** Inserting millions of already available rows one by one causes repeated random traversal and splits. A bulk loader can:

1. sort entries by search key;
2. pack leaf pages sequentially, leaving chosen free space;
3. link leaves;
4. build each upper level from the child separators.

This uses sequential I/O and builds fuller pages. The trade-off is that 100% full leaves immediately split under later inserts, so a fill factor may leave headroom.

## 15.7 Static and dynamic hashing

**[SLIDE]** A hash function maps search-key values to **buckets**, normally disk pages:

$$
h:K\rightarrow B.
$$

- **Hash index:** bucket contains index entries/RIDs.
- **Hash file organization:** bucket contains the base records.
- A collision means different keys map to the same bucket; bucket contents must be searched.
- Bucket overflow comes from too few buckets, duplicate/skewed keys, or a poor hash function.
- **Overflow chaining** links extra pages to a home bucket.

Static hashing fixes the bucket set, so growth creates long overflow chains and over-allocation wastes space. Dynamic approaches include periodic rehashing, linear hashing, and extendible hashing.

**[CORE SUPPLEMENT—algorithm named but not developed in the supplied deck] Extendible hashing:**

- hash bits index a directory of size $2^d$, where $d$ is **global depth**;
- each bucket has a **local depth**;
- on overflow, split the bucket and increase its local depth;
- if its old local depth equaled global depth, double the directory first;
- redistribute only that bucket's records using the additional hash bit.

Equality lookup is expected $O(1)$ bucket I/O plus overflow effects. Hashing does not preserve order, so `BETWEEN`, minimum/maximum, and prefix-order traversal favor a B+ tree.

## 15.8 Composite and multiple-key indexes

For a B+ tree on `(A, B, C)`, the sorted order usually supports the **leftmost prefix**:

- `A = ?` — useful;
- `A = ? AND B = ?` — useful;
- `A = ? AND B BETWEEN ...` — useful; later `C` may mostly be residual filtering;
- `B = ?` without `A` — normally cannot seek efficiently from the root.

An **index intersection** can obtain RID sets from separate indexes and intersect them; an index union can combine disjunctive predicates. A covering index contains every column needed by a query, avoiding base-table lookup, but widens the index and increases write cost.

## 15.9 Bitmap indexes

**[SLIDE]** For each distinct value $v$, maintain a bit vector with one bit per record: bit $i=1$ iff record $i$ has value $v$. Boolean conditions become word-parallel AND, OR, and NOT operations.

Example for attributes `color` and `type`:

~~~text
red:     1 0 1 0 1 0 0 0
laser:   0 0 1 1 0 0 1 0
red AND laser
         0 0 1 0 0 0 0 0
~~~

Bitmaps are especially effective for low/moderate-cardinality analytic predicates and counts. Frequent individual row updates can make them expensive or contentious. Compression can make sparse bitmaps far smaller than the uncompressed “one bit per row per value” picture.

## 15.10 Write-optimized indexes

**[SLIDE]**

### LSM tree

1. Write new entries to an in-memory sorted structure/memtable (level 0).
2. Flush it as a sorted on-disk run when full.
3. Merge/compact runs into progressively larger levels.
4. Search the memory component and relevant disk runs, commonly using Bloom filters to avoid fruitless reads **[Bloom-filter detail: core supplement]**.
5. Represent deletion using a tombstone; compaction later removes obsolete versions.

Benefits: sequential/batched writes and high ingestion throughput. Costs: read amplification across components, space amplification during compaction, and write amplification from repeated merging. A stepped/tiered variant reduces write merging but makes reads search more runs.

### Buffer tree

Internal B+ tree nodes buffer updates. When a buffer fills, updates are batch-pushed to children. This retains an ordered tree while amortizing random writes; compared with an LSM tree, it may perform more random I/O.

## 15.11 Spatial and temporal indexes

**[SLIDE]**

- **k-d tree:** recursively partitions points by alternating dimensions; its disk-oriented extension is the k-d-B tree.
- **Quadtree:** recursively splits a 2D rectangle into four quadrants until a capacity condition is met.
- **R-tree:** a height-balanced tree over minimum bounding rectangles. Child boxes may overlap, so a query may follow multiple branches.

R-tree point/region search descends into every child bounding box that intersects the query. Overlap increases search work.

Temporal tuples may have validity intervals `(start, end)`. A current-record index can treat `end = infinity` specially, while historical interval queries require an interval/temporal access method; ordinary indexing only on start time may retrieve many false candidates.

## 15.12 Index-definition SQL and selection checklist

~~~sql
CREATE INDEX idx_movie_studio_year
    ON Movie(studio, year);

CREATE UNIQUE INDEX idx_exec_certno
    ON MovieExec(certno);

DROP INDEX idx_movie_studio_year;
~~~

The exact `DROP INDEX`, clustering, filtered/partial, bitmap, and index-method syntax is DBMS-specific.

Before suggesting an index in a viva, ask:

1. Is the workload equality, range/order, full-text, spatial, or analytic Boolean filtering?
2. What is predicate selectivity?
3. Which columns form the useful prefix?
4. Is clustering important?
5. Can the index cover the query?
6. How often are the indexed columns inserted/updated/deleted?
7. How large is the structure and does it fit/cycle through cache?
8. Could partitioning or a sequential scan be cheaper?

**One-line comparison:** B+ tree gives logarithmic equality plus ordered range access; hashing gives expected constant-time equality but no order; bitmap gives extremely fast word-parallel combination for analytic dimensions; LSM optimizes sustained writes at the cost of compaction and multi-run reads.

---

# 16. Query Processing

## 16.1 From SQL text to tuples

**[SLIDE]** The main stages are:

1. **Parsing and semantic analysis:** check syntax, resolve table/column names, types, privileges, and expand views.
2. **Translation:** build an internal logical expression, commonly relational algebra.
3. **Rewrite:** apply equivalence rules and simplify predicates/expressions.
4. **Optimization:** enumerate promising physical plans and estimate their costs.
5. **Execution:** run the chosen operators and return tuples.

A **logical plan** says *which relational operations* to perform. A **physical/evaluation plan** additionally says the access path and algorithm—table scan or index scan, hash join or merge join, join order, materialization or pipeline, degree of parallelism, and so on.

## 16.2 Cost notation from the deck

**[SLIDE]**

- $n_r$: number of tuples in relation $r$.
- $b_r$: number of disk pages/blocks containing $r$.
- $M$: buffer pages available to the operator.
- $h_i$: height/page levels of index $i$.
- $t_T$: time to transfer one page.
- $t_S$: time for one seek.
- $b_b$: blocks moved at once in a buffered run.

The teaching cost model is:

$$
T\approx (\text{block transfers})t_T+(\text{seeks})t_S.
$$

The decks deliberately ignore CPU and final-output write cost in many formulas. A real optimizer also considers CPU, cache, parallelism, network, device type, buffer residency, output latency, and contention. Always state the model before quoting a cost.

## 16.3 Selection algorithms A1–A10

**[SLIDE]** The labels below match the query-processing deck.

### A1: linear scan

Scan all $b_r$ pages and test every tuple:

$$
\text{cost}=b_r\text{ transfers}+1\text{ seek}.
$$

For equality on a key, an average successful scan may stop halfway, about $b_r/2$ transfers. A1 works with any predicate and without any index.

### A2: clustering index, equality on a key

Traverse the height-$h_i$ index and fetch the one data page:

$$
(h_i+1)(t_T+t_S).
$$

This simplified formula assumes each level/data access may cause a seek and transfer; cached upper levels reduce actual I/O.

### A3: clustering index, equality on a nonkey

Matching records occupy $b$ consecutive data pages:

$$
h_i(t_T+t_S)+t_S+b\,t_T.
$$

### A4: secondary index, equality

For a unique search key, cost resembles A2. For a nonunique search key with $m$ matching records scattered across pages, worst-case data access approaches $m(t_T+t_S)$ after the index traversal. This can be more expensive than scanning.

### A5/A6: comparison using clustering/secondary index

- With data ordered on $A$, `A >= v` can seek to the first qualifying row and scan forward.
- For `A <= v`, a scan from the beginning may be cheaper than first traversing the index because the qualifying prefix starts at the first page.
- A secondary ordered index can enumerate qualifying RIDs for either direction, but scattered table lookups can dominate when selectivity is high.

### A7–A10: complex predicates

- **A7 conjunction, one index:** choose the cheapest indexed conjunct; fetch candidates; test remaining conjuncts in memory.
- **A8 conjunction, composite index:** use one index matching several conjuncts in its prefix.
- **A9 conjunction, RID intersection:** retrieve RID sets/bitmaps from several indexes and intersect them.
- **A10 disjunction, RID union:** use indexes for **every** disjunct and union the RIDs. If one disjunct has no usable index, a scan is normally needed anyway.

**Trap:** For SQL `WHERE A = 1 OR B = 2`, using only the `A` index silently misses rows satisfying only `B = 2`.

## 16.4 External merge sort

**[SLIDE]** If $b_r>M$, the relation cannot be sorted entirely in memory.

### Phase 1: create sorted runs

~~~text
for each chunk of at most M pages:
    read chunk into memory
    sort its tuples in memory
    write one sorted run
~~~

Initial number of runs:

$$
N=\left\lceil\frac{b_r}{M}\right\rceil.
$$

### Phase 2: merge

With one output buffer, at most $M-1$ input runs can be merged in one pass. Repeatedly choose the least current tuple among the input buffers, emit it, and refill an exhausted buffer. Number of merge passes:

$$
p=\left\lceil\log_{M-1}N\right\rceil.
$$

If the final output is piped to its parent instead of written, page transfers are approximately:

$$
b_r(2p+1).
$$

Reason: initial run generation reads+writes $2b_r$; each nonfinal merge reads+writes $2b_r$; final merge reads $b_r$ and streams its output.

With $b_b$ pages per input buffer, merge fan-in becomes $\lfloor M/b_b\rfloor-1$, reducing seeks by reading longer runs per request but possibly increasing the number of passes. The deck's transfer formula is:

$$
b_r\left(2\left\lceil\log_{\lfloor M/b_b\rfloor-1}(b_r/M)\right\rceil+1\right).
$$

**Worked example:** $b_r=900$, $M=100$, one-page run buffers. There are $N=9$ runs; $9\le 99$, so one merge pass suffices. Ignoring the final output write: $2(900)+900=2700$ page transfers.

## 16.5 Nested-loop joins

Let $r$ be outer and $s$ inner.

### Tuple nested loop

~~~text
for each tuple tr in r:
    for each tuple ts in s:
        if theta(tr, ts): emit concatenate(tr, ts)
~~~

**[SLIDE]** With only one page for each input, worst-case transfers are:

$$
b_r+n_r b_s,
$$

with roughly $b_r+n_r$ seeks in the deck's model. It supports an arbitrary theta condition but examines every tuple pair.

### Block nested loop

Read an outer **block/chunk**, then scan the inner relation once for that chunk:

~~~text
for each chunk C of r occupying at most M-2 pages:
    for each page Ps of s:
        join every tuple in C with every tuple in Ps
~~~

Page transfers:

$$
b_r+\left\lceil\frac{b_r}{M-2}\right\rceil b_s.
$$

Approximate seeks in the deck: $2\lceil b_r/(M-2)\rceil$. Choose the input yielding fewer chunks as outer. If one relation fits in memory as inner, both relations are read once: $b_r+b_s$ transfers.

### Indexed nested loop

If the inner input has an index on an equijoin key, probe it once per outer tuple:

$$
b_r(t_T+t_S)+n_r c,
$$

where $c$ is the cost of one inner index lookup plus matching data fetches. A small outer input and selective/cached inner index make this excellent; a large outer input plus scattered nonclustered matches makes it poor.

The deck's running example uses 5,000 student tuples/100 pages and 10,000 takes tuples/400 pages. Under its worst-case assumptions, block nested loop with student outer costs $100+100\cdot400=40{,}100$ transfers; indexed nested loop with a five-page lookup estimate costs $100+5{,}000\cdot5=25{,}100$ transfers/seeks. The numbers are teaching estimates, not universal rankings.

## 16.6 Sort-merge join

**[SLIDE]** Applicable to equijoins/natural joins:

1. sort each unsorted input by join key;
2. scan both sorted streams together;
3. when keys match, produce the cross-product of duplicate-key groups;
4. advance the side with the smaller key otherwise.

If both are already sorted and each duplicate group fits in memory, merge cost is:

$$
b_r+b_s\text{ transfers}
+\left\lceil\frac{b_r}{b_b}\right\rceil
+\left\lceil\frac{b_s}{b_b}\right\rceil\text{ seeks}.
$$

Add external-sort cost for unsorted inputs. Sort-merge is attractive when sorted output is useful later or inputs already arrive ordered. Duplicate groups larger than memory require careful mark/restore or spilling.

## 16.7 Grace hash join and hybrid hash join

**[SLIDE]** Hash join applies to equality/natural joins. Use the smaller relation $s$ as **build input** and $r$ as **probe input**.

### Partition phase

~~~text
for tuple s in build:
    write s to partition S[h1(s.join_key)]
for tuple r in probe:
    write r to partition R[h1(r.join_key)]
~~~

Tuples that can join must enter corresponding partitions because equal join keys hash equally.

### Build/probe phase

~~~text
for each partition i:
    build an in-memory hash table over S[i] using hash h2
    for each tuple r in R[i]:
        probe h2(r.join_key)
        emit every matching pair
~~~

Choose about $\lceil b_s/M\rceil$ partitions times a safety/fudge factor (the deck uses roughly 1.2), so each build partition fits memory. If there are too many partitions for output buffers, recursively repartition using another hash function. Skew or many identical keys can overflow a partition; recursively partition when possible, otherwise fall back to a different join such as block nested loop.

Without recursive partitioning, the leading transfer cost is:

$$
3(b_r+b_s):
$$

read and write both inputs while partitioning $2(b_r+b_s)$, then read the partitions once to build/probe $(b_r+b_s)$. The deck's more detailed estimate adds partially filled output-page overhead:

$$
3(b_r+b_s)+4n_h
$$

transfers and approximately

$$
2\left(\left\lceil b_r/b_b\right\rceil+
\left\lceil b_s/b_b\right\rceil\right)
$$

seeks. If the whole build side fits memory, skip partitioning and read each input once: $b_r+b_s$.

**Hybrid hash join** retains one build partition in memory while partitioning, and probes that partition immediately; those pages avoid being written and reread. The deck's example reduces 1,500 transfers for an ordinary hash join to 1,300.

## 16.8 Implementing other relational operations

**[SLIDE]**

- **Duplicate elimination:** sort so duplicates become adjacent, or hash so equal tuples reach one bucket. Remove duplicates during initial runs/partial hash tables to shrink later work.
- **Projection:** discard columns; if SQL/relational semantics require duplicate elimination, sort or hash afterward.
- **Aggregation/grouping:** sort or hash on group keys. Push **partial aggregation** early: keep `sum`, `count`, `min`, and `max`; compute `avg` from global sum/global count, not by averaging partial averages.
- **Set union/intersection/difference:** sort-merge both inputs or partition them with the same hash function and process corresponding partitions.
- **Outer join:** run a join while marking matches; emit unmatched preserved-side rows padded with NULLs.

## 16.9 Materialization and pipelining

**[SLIDE]**

- **Materialization:** fully compute an intermediate relation, store it, then let its parent read it. Always possible but adds write/read I/O and latency.
- **Pipelining:** send a tuple to the parent as soon as it is produced. Avoids temporary storage and can return first rows early.

In the pull/demand-driven **iterator model**, every operator supports:

~~~text
open()   -- allocate/initialize state and open children
next()   -- return the next tuple or EOF, preserving state
close()  -- release resources and close children
~~~

Producer-driven/push execution has a child eagerly place tuples in an inter-operator buffer; it blocks under backpressure when the buffer fills.

**Blocking operator:** cannot produce its final-kind output until enough/all input arrives, for example full sort, duplicate elimination, and ordinary hash aggregation. Operators can still be split into pipeline stages: external sort has run generation/merge; Grace hash join has partition/build-probe; hybrid hash join outputs matches for its in-memory partition early.

Double buffering overlaps computation with I/O: fill buffer B while buffer A is being written/read by the device.

## 16.10 A physical-join decision answer

If asked “Which join is best?”, reject the premise politely: no algorithm is universally best.

- arbitrary theta predicate and small input: nested loop;
- small outer + selective inner index: indexed nested loop;
- equijoin, no useful order, build side fits/partitions well: hash join;
- equijoin with ordered inputs or ordered output needed: merge join;
- severe hash skew or non-equality condition: sort/loop alternatives;
- final decision depends on estimated cardinality, pages, memory, clustering, cache, and required output order.

---

# 17. Query Optimization

## 17.1 Why logically identical SQL can differ by days

**[SLIDE]** Relational expressions have many equivalent forms, and each operator has several physical algorithms. The optimizer:

1. generates promising equivalent logical expressions;
2. assigns physical implementations/access paths;
3. estimates intermediate cardinalities and costs;
4. selects the cheapest estimated plan.

Optimization itself has a budget; enumerating every expression and physical combination is exponential, so real systems use pruning, dynamic programming, heuristics, memo structures, and time limits.

## 17.2 `EXPLAIN` versus execution

**[SLIDE]**

~~~sql
-- Oracle style
EXPLAIN PLAN FOR
SELECT * FROM Movie WHERE year >= 2020;
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- PostgreSQL style; actually runs the query
EXPLAIN ANALYZE
SELECT * FROM Movie WHERE year >= 2020;
~~~

`EXPLAIN` normally reports estimates and the selected plan without executing the data-producing statement. `EXPLAIN ANALYZE` executes and reports actual timing/rows, so do not run it casually on a destructive statement or huge workload. PostgreSQL-style cost `f..l` means estimated startup cost to first row and total cost to all rows, not wall-clock milliseconds.

## 17.3 Core equivalence rules

**[SLIDE]** Let $E,E_1,E_2$ be expressions.

1. Split conjunctive selection:

$$
\sigma_{p\land q}(E)\equiv\sigma_p(\sigma_q(E)).
$$

2. Selections commute:

$$
\sigma_p(\sigma_q(E))\equiv\sigma_q(\sigma_p(E)).
$$

3. Collapse nested projections when the outer attribute set is a subset:

$$
\pi_{L_1}(\pi_{L_2}(E))\equiv\pi_{L_1}(E),\quad L_1\subseteq L_2.
$$

4. Convert product plus predicate to theta join:

$$
\sigma_p(E_1\times E_2)\equiv E_1\bowtie_p E_2.
$$

5. Inner/natural joins commute and associate, subject to correctly relocating predicates:

$$
E_1\bowtie E_2\equiv E_2\bowtie E_1,
$$

$$
(E_1\bowtie E_2)\bowtie E_3\equiv E_1\bowtie(E_2\bowtie E_3).
$$

6. Push a selection into the side containing all attributes it references:

$$
\sigma_p(E_1\bowtie E_2)\equiv(\sigma_p(E_1))\bowtie E_2.
$$

7. Push projection while retaining every output and join-predicate attribute. Dropping a join key early changes or makes the query impossible.

8. A selection on grouping keys can be pushed below grouping; a predicate on an aggregate value normally remains HAVING/above aggregation.

**Outer-join warning:** left/right outer joins are not freely commutative or associative like inner joins. A predicate on the null-supplying side can reject all NULL-extended rows and effectively turn an outer join into an inner join. Apply only a proven null-rejecting equivalence.

## 17.4 Why “push selections and projections down” works

Early selection reduces the **number of tuples**; early projection reduces their **width**. Both shrink page counts of later joins, sorts, and hashes. But correctness comes first:

- keep attributes used by later predicates, joins, grouping, and output;
- do not push a volatile/side-effecting expression where evaluation count matters;
- outer joins, NULLs, duplicate/bag semantics, aggregation, and constraints can limit rewrites.

## 17.5 Catalog statistics

**[SLIDE]**

- $n_r$: tuples in $r$.
- $b_r$: pages of $r$.
- $l_r$: bytes per tuple.
- $f_r$: blocking factor, tuples/page; approximately $b_r=\lceil n_r/f_r\rceil$.
- $V(A,r)$: number of distinct values of attribute $A$ in $r$.
- `min`, `max`, NULL fraction, most-common values, and histograms.

An **equi-width histogram** divides the value range into equal-width buckets. An **equi-depth histogram** makes buckets contain roughly equal tuple counts. Most-common-value statistics preserve heavy hitters that a uniform model would miss.

## 17.6 Selection-cardinality estimation

Under a uniform distribution:

$$
|\sigma_{A=v}(r)|\approx\frac{n_r}{V(A,r)}.
$$

If $A$ is a key, the answer is at most one. For `A <= v` under a continuous uniform range:

$$
|\sigma_{A\le v}(r)|\approx
n_r\frac{v-\min(A)}{\max(A)-\min(A)},
$$

clamped to $[0,n_r]$. Without statistics, the deck uses a crude $n_r/2$ range estimate.

Let $s_i$ be selectivity (probability) of predicate $p_i$. Assuming independence:

$$
|\sigma_{p_1\land\cdots\land p_k}(r)|
\approx n_r\prod_i s_i,
$$

$$
|\sigma_{p_1\lor\cdots\lor p_k}(r)|
\approx n_r\left(1-\prod_i(1-s_i)\right),
$$

$$
|\sigma_{\neg p}(r)|\approx n_r(1-s_p).
$$

The independence assumption is often wrong: `city = 'Dhaka'` and `country = 'Bangladesh'` are correlated. Multi-column statistics, constraints, and sampling improve estimates.

## 17.7 Join-cardinality estimation

For equijoin $r\bowtie_{r.A=s.A}s$, assuming containment/uniformity:

$$
|r\bowtie s|\approx
\frac{n_r n_s}{\max(V(A,r),V(A,s))}.
$$

If every foreign-key value in $s.A$ references the unique primary key $r.A$, then an inner join preserving all non-NULL referencing rows has approximately/exactly $n_s$ rows, adjusted for nullable/dangling values allowed by the schema.

The deck example has `student.ID` as primary key with 5,000 values and `takes.ID` with 10,000 rows/2,500 distinct values:

$$
\frac{5000\cdot10000}{\max(5000,2500)}=10000.
$$

Bad cardinality estimates multiply up a join tree. Underestimating one early join can cause the optimizer to choose nested loops and tiny memory where a hash join and spill budget were needed.

Other slide estimates:

- $|\pi_A(r)|\approx V(A,r)$ under duplicate elimination;
- number of groups for `GROUP BY G` is $V(G,r)$;
- union upper bound $|r|+|s|$;
- intersection upper bound $\min(|r|,|s|)$;
- difference upper bound $|r|$.

## 17.8 Join-order optimization

For $k$ relations, join orders grow rapidly. A left-deep dynamic program **[CORE SUPPLEMENT—the deck lists dynamic programming but does not develop the algorithm]** can keep the cheapest plan for every subset:

~~~text
for each single relation R:
    best[{R}] = cheapest access path for R

for size = 2 .. k:
    for each subset S of that size:
        best[S] = infinity
        for each relation R in S:
            candidate = Join(best[S - {R}], best[{R}])
            cost candidate with each applicable join algorithm
            retain cheapest candidate for S
~~~

The **principle of optimality** permits discarding a more expensive subplan only when it has the same required physical properties (such as output order) as the cheaper one. A slightly more expensive subplan that produces useful order may make the entire query cheaper.

- **Left-deep tree:** right child is usually a base access; easy to pipeline and suits index nested loops.
- **Bushy tree:** both children can be joins; may expose parallelism and smaller intermediates but enlarges search.

## 17.9 Materialized views

**[SLIDE]** A materialized view stores a query result, trading storage/update work for faster reads.

~~~sql
-- Conceptual form; exact syntax/refresh options are vendor-specific
CREATE MATERIALIZED VIEW DepartmentSalary AS
SELECT dept_name, SUM(salary) AS total_salary
FROM Instructor
GROUP BY dept_name;
~~~

Maintenance choices:

- full recomputation;
- scheduled/periodic refresh;
- on-commit refresh;
- **incremental view maintenance** using base-table deltas.

For $v=r\bowtie s$, inserting delta $\Delta r^+$ changes the view by:

$$
\Delta v^+=(\Delta r^+)\bowtie s.
$$

Deleting $\Delta r^-$ analogously removes $(\Delta r^-)\bowtie s$, subject to bag multiplicities and simultaneous deltas. Triggers can implement maintenance, but built-in mechanisms can coordinate correctness and optimization better.

## 17.10 Optimizer viva traps

- “An index always makes a query faster.” False; low selectivity and random base-row fetches can make a scan cheaper.
- “The optimizer finds the mathematically optimal plan.” Usually false; it finds the best estimated plan inside a bounded search/model.
- “Two equivalent relational-algebra expressions always have the same cost.” Same result, potentially radically different intermediate sizes and I/O.
- “`EXPLAIN` actual rows are available without execution.” Not normally; estimates are not actuals.
- “Projection pushdown can discard any unselected column.” It must retain later join/filter/group/order columns.
- “More accurate statistics change query results.” They should change plans, not relational semantics.

---

# 18. Transactions, Schedules, and Serializability

## 18.1 Transaction and ACID

**[SLIDE]** A transaction is a logical unit of program execution that reads and possibly updates database items.

Fund transfer of 50 from A to B:

~~~text
read(A)
A = A - 50
write(A)
read(B)
B = B + 50
write(B)
commit
~~~

- **Atomicity:** all effects happen or none do. A crash after debit must not lose money.
- **Consistency:** if the transaction starts in a valid state and its logic is correct, it preserves declared/business invariants, e.g. `A+B` unchanged. Consistency is a joint responsibility of constraints, correct transaction logic, and isolation—not magic performed solely by the DBMS.
- **Isolation:** concurrent outcome appears as allowed by the chosen isolation model, ideally equivalent to some serial execution.
- **Durability:** after commit is acknowledged, effects survive failures covered by the recovery model.

Atomicity concerns failure within a transaction; isolation concerns interference among transactions. Durability begins at commit; consistency is the application/schema property the other mechanisms help protect.

## 18.2 Transaction states

**[SLIDE]**

~~~text
active -> partially committed -> committed -> terminated
   |              |
   +-----------> failed -> aborted -> terminated
                                \\-> restarted (new execution)
~~~

- **Active:** executing.
- **Partially committed:** last statement ran, but commit is not yet durable.
- **Committed:** commit record/effects satisfy durability protocol.
- **Failed:** cannot continue normally.
- **Aborted:** effects have been rolled back.

After abort, a transaction may be retried if failure was transient, or terminated if its input/logic is invalid. A compensating transaction semantically reverses an already committed business action; it is not identical to low-level rollback.

## 18.3 Why concurrency?

**[SLIDE]** Concurrent execution improves CPU/device utilization and throughput and lets short transactions avoid waiting behind long ones. It also introduces lost updates, dirty reads, inconsistent analysis, nonrepeatable reads, phantoms, and deadlocks. Concurrency control aims to preserve a useful correctness criterion while permitting overlap.

## 18.4 Schedules

**[SLIDE]** A schedule interleaves operations from several transactions while preserving the program order inside each transaction.

- **Serial schedule:** one complete transaction followed by another; correct if each transaction is correct, but low concurrency.
- **Serializable schedule:** interleaved yet equivalent under a specified notion to a serial schedule.
- `r_i(X)` means transaction $T_i$ reads item X; `w_i(X)` writes it; `c_i` commits; `a_i` aborts.

## 18.5 Conflicts

Operations of different transactions conflict iff they access the same item and at least one writes:

| First | Second | Conflict? |
|---|---|---:|
| `r_i(X)` | `r_j(X)` | no |
| `r_i(X)` | `w_j(X)` | yes |
| `w_i(X)` | `r_j(X)` | yes |
| `w_i(X)` | `w_j(X)` | yes |

Swapping adjacent nonconflicting operations does not change what either transaction reads/writes. A schedule is **conflict serializable** if such swaps can transform it into a serial schedule.

## 18.6 Precedence/conflict graph algorithm

**[SLIDE]**

~~~text
build_graph(schedule):
    create one vertex per transaction
    for each pair of operations op_i before op_j:
        if i != j and both touch the same item
           and at least one is a write:
            add edge Ti -> Tj

if graph contains a directed cycle:
    schedule is NOT conflict serializable
else:
    schedule is conflict serializable
    any topological order is an equivalent serial order
~~~

Efficient construction tracks the last writer and prior readers per item instead of testing every operation pair. Cycle detection/topological sort is $O(V+E)$; the deck also mentions a simpler $O(V^2)$ bound.

### Worked schedule

~~~text
r1(A) w1(A) r2(A) r2(B) w2(B) r3(B) w3(B) c1 c2 c3
~~~

- `w1(A)` before `r2(A)` gives $T_1\to T_2$.
- `w2(B)` before `r3(B)`/`w3(B)` gives $T_2\to T_3$.
- No reverse edge exists.

Graph is acyclic; topological/serial order is $T_1,T_2,T_3$.

Cycle example:

~~~text
r1(A) w1(A) r2(B) w2(B) r1(B) w1(B) r2(A) w2(A)
~~~

Conflicts on A give $T_1\to T_2$; conflicts on B give $T_2\to T_1$. The cycle proves it is not conflict serializable.

## 18.7 View serializability

**[SLIDE]** Schedules S and S' are view-equivalent when, for every item:

1. the same transactions read its initial value;
2. each read obtains its value from the same writer transaction;
3. the same transaction performs the final write.

A schedule is **view serializable** if view-equivalent to a serial schedule. Every conflict-serializable schedule is view-serializable, but the converse fails when blind writes occur. Testing general view serializability is NP-complete, while conflict serializability has the polynomial graph test. Therefore practical protocols usually target conflict serializability or another efficiently enforceable model.

**Blind write:** a transaction writes X without first reading X. It can make two schedules view-equivalent even when their write-write conflicts cannot be swapped into the corresponding serial order.

## 18.8 Recoverable, cascadeless, and strict schedules

**[SLIDE + CORE DETAIL]**

- **Recoverable:** if $T_j$ reads a value written by $T_i$, then $T_i$ commits before $T_j$ commits.
- **Cascadeless:** if $T_j$ reads a value written by $T_i$, then $T_i$ commits before that read. No dirty reads, hence no cascading aborts.
- **Strict:** after $T_i$ writes X, no other transaction may read or write X until $T_i$ commits/aborts. This avoids dirty reads and dirty writes and greatly simplifies recovery.

Relationship:

$$
\text{strict}\Rightarrow\text{cascadeless}\Rightarrow\text{recoverable}.
$$

Examples:

~~~text
-- unrecoverable
w1(X) r2(X) c2 a1

-- recoverable but cascading abort is possible
w1(X) r2(X) c1 c2

-- cascadeless
w1(X) c1 r2(X) c2
~~~

Serializability and recoverability answer different questions: serializability controls equivalence of interleaving; recoverability controls commit/abort dependencies after one transaction reads another's write.

## 18.9 Common anomalies

| Anomaly | Minimal idea |
|---|---|
| Dirty read | T2 reads T1's uncommitted value; T1 aborts |
| Dirty write | T2 overwrites T1's uncommitted write |
| Lost update | both read old X; later write overwrites earlier update |
| Nonrepeatable read | T1 reads the same row twice and sees different committed values |
| Phantom | repeated predicate query returns a changed set because rows were inserted/deleted/updated into range |
| Incorrect summary | aggregate mixes values from before and after another multirow transaction |
| Write skew | two transactions read same snapshot and update different rows, jointly breaking an invariant |

**Lost-update trace:**

~~~text
X = 100
T1: read X=100             T2: read X=100
T1: X=X+10; write 110      T2: X=X-20; write 80
final X=80; T1's +10 vanished
~~~

## 18.10 SQL isolation levels

**[SLIDE + CORE DETAIL]** Standard level guarantees are often summarized as:

| Isolation level | Dirty read | Nonrepeatable read | Phantom |
|---|---:|---:|---:|
| Read uncommitted | possible | possible | possible |
| Read committed | prevented | possible | possible |
| Repeatable read | prevented | prevented | standard permits possible |
| Serializable | prevented | prevented | prevented |

This table is a minimum-guarantee abstraction. Actual mechanisms and anomalies vary by DBMS: a snapshot-based repeatable-read level may prevent classic phantoms yet allow write skew; “serializable” should guarantee serializable outcomes even if implemented without predicate locks.

## 18.11 SQL transaction syntax

~~~sql
-- Syntax details vary across products
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

UPDATE Account SET balance = balance - 50 WHERE id = 'A';
UPDATE Account SET balance = balance + 50 WHERE id = 'B';

COMMIT;      -- make the unit durable
-- or ROLLBACK;
~~~

Safer application pattern:

~~~text
begin transaction
try:
    debit exactly one source row
    credit exactly one destination row
    verify business conditions
    commit
catch transient serialization/deadlock error:
    rollback
    retry the WHOLE transaction with bounded backoff
catch any other error:
    rollback
    report failure
~~~

**[CORRECTION]** The transaction deck says statements commit implicitly by default in almost all systems. More precise: many drivers/tools offer an **autocommit mode**, often enabled by default, in which each successful statement is a transaction; server/client defaults vary. Oracle DML in an ordinary explicit session is not universally “committed after every successful statement.” DDL may cause implicit commits in some products. State the specific DBMS/client.

---

# 19. Concurrency-Control Protocols

## 19.1 Shared and exclusive locks

**[SLIDE]**

- **S/shared lock:** permits reading.
- **X/exclusive lock:** permits reading and writing.

Compatibility:

| Held \ Requested | S | X |
|---|---:|---:|
| S | yes | no |
| X | no | no |

Many readers may hold S simultaneously; an X holder excludes all others. The lock manager keeps granted locks and a wait queue per item, plus often a list of locks per transaction for fast cleanup.

Locking individual reads and immediately unlocking is not enough: another transaction can change data between related reads, producing a nonserializable schedule.

## 19.2 Two-phase locking (2PL)

**[SLIDE]**

- **Growing phase:** acquire/upgrade locks; release none.
- **Lock point:** instant the transaction obtains its final lock.
- **Shrinking phase:** release/downgrade locks; acquire none.

All schedules generated by basic 2PL are conflict serializable; serial order follows lock-point order. However, 2PL can deadlock and basic 2PL can allow cascading rollback.

Variants:

| Protocol | Rule | Consequence |
|---|---|---|
| Basic 2PL | growing then shrinking | conflict serializable; deadlock possible |
| Strict 2PL | hold all X locks to commit/abort | strict, recoverable, no cascading abort from dirty data |
| Rigorous 2PL | hold all S and X locks to commit/abort | commit order is serialization order |
| Conservative/static 2PL **[supplement]** | obtain every required lock before starting | deadlock-free, but locks/needs must be known and concurrency is lower |

Two important logical statements:

- 2PL is **sufficient**, not necessary, for conflict serializability; some conflict-serializable schedules cannot be produced under 2PL.
- Strictness alone and serializability are different; strict 2PL provides both because it includes the 2PL discipline and strict X-lock retention.

## 19.3 Lock conversion

**[SLIDE]**

- Upgrade S→X is allowed only during growing phase and waits until no incompatible holder remains.
- Downgrade X→S is allowed during shrinking phase.

Two transactions that both hold S and both try to upgrade to X can deadlock. Update locks or ordered access can reduce this pattern **[implementation supplement]**.

## 19.4 Deadlock and starvation

**[SLIDE + CORE SUPPLEMENT]** Deadlock means a set of transactions waits cyclically, so none can progress.

~~~text
T1 holds X(A), requests X(B)
T2 holds X(B), requests X(A)
~~~

The **wait-for graph** has one vertex per active transaction and edge $T_i\to T_j$ when $T_i$ waits for a lock held by $T_j$. A directed cycle means deadlock for single-instance locks.

Handling strategies:

1. **Detection and recovery:** periodically/when waiting, detect a cycle; abort a victim; release its locks; roll it back/restart it.
2. **Timeout:** abort a transaction that waits too long. Simple, but confuses slow execution with deadlock.
3. **Resource/lock ordering:** acquire items in a global order; eliminates cycles when consistently obeyed.
4. **Wait-die:** older requester waits for younger holder; younger requester aborts (“dies”) when holder is older. Nonpreemptive.
5. **Wound-wait:** older requester aborts (“wounds”) younger holder; younger requester waits for older holder. Preemptive.

Keep the same original timestamp on retry in wait-die/wound-wait to avoid starvation. Victim selection can consider work completed, locks held, rollback cost, and prior abort count.

**Starvation** is indefinite postponement without necessarily a wait cycle—for example, an X-lock waiter is repeatedly bypassed by new S-lock requests. Fair queues/aging and bounded victimization address it.

## 19.5 Multiple granularity and intention locks

**[CORE SUPPLEMENT—the concurrency deck lists this in its outline but the supplied slide file does not develop it]** Locking a table is cheap but coarse; locking every row is precise but expensive. A hierarchy can be:

~~~text
database -> table -> page -> row
~~~

Intention modes advertise planned descendant locks:

- **IS:** intends S below.
- **IX:** intends X below.
- **SIX:** S on this node plus intends X below.

Compatibility:

| Held \ Requested | IS | IX | S | SIX | X |
|---|---:|---:|---:|---:|---:|
| IS | yes | yes | yes | yes | no |
| IX | yes | yes | no | no | no |
| S | yes | no | yes | no | no |
| SIX | yes | no | no | no | no |
| X | no | no | no | no | no |

Protocol: acquire locks top-down; release bottom-up under the chosen 2PL rule. To X-lock one row, obtain IX on its ancestors then X on the row. A transaction requesting S on the table conflicts with another's IX, so the system detects hidden row writers without scanning every row lock.

**Lock escalation:** replace many fine-grained locks with one coarse lock. It reduces lock-table overhead but may reduce concurrency.

## 19.6 Phantom protection

Row locks alone do not protect absence/ranges:

~~~text
T1: SELECT * FROM Instructor WHERE salary > 90000;
T2: INSERT a new Instructor with salary 100000; COMMIT;
T1: repeat query -> an extra row appears
~~~

To serialize predicate access, use predicate locks conceptually or implementation techniques such as key-range/next-key locks on the relevant index gaps. Locking only rows that already exist cannot prevent a row from appearing in the predicate range.

## 19.7 Timestamp ordering

**[CORE SUPPLEMENT—named by the concurrency outline, not developed in the supplied slides]** Give each transaction a unique timestamp `TS(T)`. Each item X tracks:

- `readTS(X)`: largest timestamp of any transaction that read X;
- `writeTS(X)`: largest timestamp of any transaction that wrote X.

Basic rules:

~~~text
read_T(X):
    if TS(T) < writeTS(X): abort/restart T
    else read X; readTS(X) = max(readTS(X), TS(T))

write_T(X):
    if TS(T) < readTS(X): abort/restart T
    if TS(T) < writeTS(X): abort/restart T
        -- Thomas write rule may ignore this obsolete write instead
    else write X; writeTS(X) = TS(T)
~~~

This enforces timestamp order and does not wait, so it avoids deadlock; repeated aborts/starvation and cascading/recovery issues require further rules. **Thomas's write rule** ignores an obsolete write when a newer write already exists, permitting some view-serializable schedules beyond basic conflict serializability.

## 19.8 Optimistic/validation-based control

**[CORE SUPPLEMENT—named by the outline]** Assume conflicts are rare:

1. **Read phase:** read database and write tentative values privately.
2. **Validation phase:** verify the transaction does not conflict with overlapping committed/validated transactions.
3. **Write phase:** install tentative changes if validation passes; otherwise abort/retry.

It avoids lock waiting and deadlock, fitting low-contention/read-mostly workloads. High contention wastes work through validation failures.

## 19.9 MVCC and snapshot isolation

**[SLIDE + CORE DETAIL]** Multi-version concurrency control keeps several committed versions. A transaction reads a version visible to its snapshot rather than blocking a concurrent writer.

Under **snapshot isolation (SI)**:

- transaction reads a snapshot of committed data as of its start;
- it sees its own writes;
- concurrent commits after its snapshot are invisible to its reads;
- first-committer-wins (or first-updater-wins) aborts overlapping transactions that write the same item.

Consequently SI prevents dirty reads, nonrepeatable reads within the snapshot, and ordinary lost updates from concurrent writes to the same row. It is **not necessarily serializable**.

### Write-skew example

Invariant: at least one doctor must remain on call.

~~~text
Initially: Alice=ON, Bob=ON

T1 snapshot sees Bob=ON; writes Alice=OFF
T2 snapshot sees Alice=ON; writes Bob=OFF
They update different rows, so no write-write conflict.
Both commit -> nobody is ON -> invariant violated.
~~~

This is not a lost update: neither overwrote the other's row. It is write skew caused by read-write dependencies across different items.

**Serializable Snapshot Isolation (SSI)** tracks dangerous read-write dependency patterns and aborts transactions where a serialization cycle could form. The supplied deck notes PostgreSQL's SSI and index/range conflict tracking for phantoms.

**[CORRECTION]** The deck makes version-specific claims about particular DBMS products. Treat those as historical examples. For a viva, explain the mechanism and state that exact implementation/default isolation must be checked for the product/version.

## 19.10 Locking versus MVCC

| Question | Locking/strict 2PL | MVCC/snapshot family |
|---|---|---|
| Reader vs writer | may block depending on mode | readers often use old version and do not block writer |
| Deadlock | possible among locks | still possible for writers/other locks |
| Version storage | little for ordinary reads | old versions need space and garbage collection |
| Serializable implementation | rigorous discipline/range locks | SSI, serializable validation, or other dependency control |
| Typical risk | blocking/deadlock | write skew/version bloat if weaker SI |

MVCC is a storage technique, not by itself an isolation level; it can implement read committed, snapshot isolation, or serializable behavior depending on visibility and conflict rules.

---

# 20. Recovery

> **[CORE SUPPLEMENT—source boundary]** The two current merged DBMS sources end their detailed sequence at transactions/concurrency and do not contain a full recovery chapter. This section is standard viva-core material, not attributed to a missing slide unit.

## 20.1 Failure classes

- **Transaction failure:** constraint error, explicit abort, deadlock victim, arithmetic/application error.
- **System crash:** power/OS/DBMS failure loses volatile memory but persistent pages/log survive.
- **Media failure:** disk/page corruption or device loss destroys persistent data.
- **Communication/site failure:** important in distributed transactions.

Recovery must preserve atomicity and durability while respecting the buffer policy.

## 20.2 STEAL/NO-STEAL and FORCE/NO-FORCE

- **STEAL:** buffer manager may write a dirty page containing an uncommitted transaction's change. Needs **UNDO** after abort/crash.
- **NO-STEAL:** such a page cannot reach disk before commit. Avoids crash UNDO but may require a huge buffer for long transactions.
- **FORCE:** every page changed by a transaction is forced to disk at commit. Avoids REDO but makes commit expensive/random.
- **NO-FORCE:** commit can return before all changed data pages reach disk. Needs **REDO** after crash.

| Buffer policy | Recovery need |
|---|---|
| NO-STEAL + FORCE | neither ordinary UNDO nor REDO |
| STEAL + FORCE | UNDO |
| NO-STEAL + NO-FORCE | REDO |
| STEAL + NO-FORCE | UNDO + REDO; common high-performance choice |

Do not confuse forcing the **log** at commit with forcing every **data page**. WAL deliberately forces a small sequential log record while allowing data pages to remain no-force.

## 20.3 Write-ahead logging (WAL)

A log record can be written as:

~~~text
<START T>
<T, X, old_value, new_value>
<COMMIT T>
<ABORT T>
~~~

WAL rules:

1. Before a dirty data page is written, every log record describing changes already reflected on that page must be durable. This preserves the old value/information needed to undo.
2. Before commit is acknowledged, the transaction's commit record and all its preceding log records must be durable. This preserves information needed to redo.

Each log record has an increasing **LSN** (log sequence number). A page's `pageLSN` identifies the newest logged update reflected on that page. During redo, skip an update when the page already has an equal/newer LSN; this makes redo idempotent.

## 20.4 Undo and redo worked trace

Initial `A=100`, `B=200`:

~~~text
LSN 10: <START T1>
LSN 20: <T1, A, 100, 90>
LSN 30: <START T2>
LSN 40: <T2, B, 200, 230>
LSN 50: <COMMIT T2>
LSN 60: <T1, B, 230, 240>
CRASH
~~~

At the crash, T2 is a **winner** and T1 a **loser**. With arbitrary STEAL/NO-FORCE page writes:

1. REDO logged history as needed: A→90, B→230, then B→240.
2. UNDO loser T1 backward: B 240→230, then A 90→100.
3. T2 remains durable: final A=100, B=230.

Why redo a loser then undo it? ARIES “repeats history” to recreate the exact precrash state, including loser effects that may have influenced later physical actions, then performs logged logical rollback.

## 20.5 Checkpoints

A checkpoint limits how far recovery scans.

- A **quiescent checkpoint** pauses new work and flushes state; simple but harms availability.
- A **fuzzy checkpoint** records active transactions and dirty-page information while transactions continue; recovery still consults log after the checkpoint.

A checkpoint does not mean every committed page is necessarily on disk, nor that everything before it can blindly be discarded. Log truncation/archival depends on the oldest page/transaction still needing undo/redo and on backup requirements.

## 20.6 ARIES overview

ARIES uses WAL, STEAL/NO-FORCE, repeating history, and compensation log records (CLRs).

### Analysis

Starting from the last checkpoint, reconstruct:

- **transaction table:** active transactions, status, last LSN;
- **dirty page table:** dirty pages and their earliest potentially unpropagated update `recLSN`.

Determine winners and losers.

### Redo

Start near the smallest `recLSN`. Repeat history in increasing LSN order. Redo a page update only when the page may not contain it, using dirty-page membership, `recLSN`, and `pageLSN` checks.

### Undo

Process losers backward by LSN, restoring before-images/logical inverse. For every undo action, write a **CLR** containing `undoNextLSN`, then eventually write transaction-end/abort. CLRs are redone but never undone, so a crash during recovery resumes safely without undoing the same action forever.

Compact algorithm:

~~~text
ANALYSIS: rebuild transaction table and dirty-page table
REDO:     scan forward, repeat missing history
UNDO:     follow loser log chains backward; write CLRs
~~~

## 20.7 Backup and media recovery

WAL cannot recreate a database whose data and log device are both destroyed without an earlier copy. Media recovery typically:

1. restore the most recent full/incremental backup;
2. replay archived and current redo logs to the desired point;
3. undo incomplete transactions if required;
4. validate consistency and resume service.

- **Full backup:** all selected data.
- **Incremental backup:** changes since a prior backup.
- **Point-in-time recovery:** stop replay before an accidental destructive event.
- Backups must be encrypted, access-controlled, geographically/failure-domain separated, retained, and—most importantly—regularly restore-tested.

## 20.8 Recovery viva answers

- **Why WAL?** Persist a compact sequential description before risky page writes/commit, enabling atomic undo and durable redo.
- **Why NO-FORCE?** Avoid forcing many random data pages at every commit; flush the sequential log instead.
- **Why STEAL?** Let the buffer evict dirty pages and support transactions larger than memory; WAL supplies undo.
- **REDO versus UNDO?** REDO reapplies committed/missing effects using after-information; UNDO reverses uncommitted effects using before-information/inverses.
- **Checkpoint versus backup?** Checkpoint accelerates crash recovery using the same database/log; backup survives media loss and supports historical restore.

---

# 21. Database Security

> **[CORE SUPPLEMENT—source boundary]** The current logical DBMS merge mentions users/permissions and Oracle credentials, but it does not contain a standalone database-security unit. The deeper material below is standard viva preparation.

## 21.1 Defense layers

Database confidentiality/integrity/availability require several controls together:

1. authenticate identities strongly;
2. authorize by least privilege using roles;
3. constrain and validate data in the DBMS;
4. use parameterized SQL;
5. encrypt transport and appropriate storage/fields/backups;
6. protect keys separately;
7. patch/harden/configure the service and host;
8. audit sensitive actions and monitor anomalies;
9. back up and test recovery;
10. separate duties and production/nonproduction data.

Encryption alone does not stop an authorized-but-malicious account from issuing a valid query, and access control alone does not protect a stolen offline disk.

## 21.2 GRANT, REVOKE, roles, and views

~~~sql
CREATE ROLE reporting_reader;

GRANT SELECT ON Movie TO reporting_reader;
GRANT reporting_reader TO analyst_user;

REVOKE SELECT ON Movie FROM reporting_reader;

CREATE VIEW PublicMovie AS
SELECT title, year, genre
FROM Movie;
GRANT SELECT ON PublicMovie TO reporting_reader;
~~~

Exact role syntax varies. Grant only required operations on required objects; applications should not connect as DBA/schema owner. Views can hide columns/rows, but robust row-level security may require product policy features, carefully secured procedures, or separate schemas.

## 21.3 SQL injection

Unsafe string concatenation:

~~~java
String sql = "SELECT * FROM Users WHERE email='" + email +
             "' AND password='" + password + "'";
~~~

Input such as `' OR '1'='1` changes code structure. Safe parameter binding:

~~~java
PreparedStatement ps = connection.prepareStatement(
    "SELECT id, password_hash FROM Users WHERE email = ?");
ps.setString(1, email);
ResultSet rs = ps.executeQuery();
~~~

Parameters separate code from data and handle escaping/types. They cannot parameterize arbitrary identifiers or SQL keywords; choose dynamic table/column/order names from an allowlist. Stored procedures are safe only when they avoid unsafe dynamic concatenation.

## 21.4 Passwords in a database

Do **not** store decryptable plaintext passwords. Store:

~~~text
algorithm/version + work factor + random salt + password-KDF output
~~~

Use a password-specific KDF such as Argon2id, scrypt, bcrypt, or PBKDF2 with current policy parameters; compare in constant time. A unique random salt defeats precomputed rainbow tables and separates equal passwords. An optional server-held pepper is stored outside the database and complicates operations/rotation.

Encryption is appropriate when the application must later recover a secret (for example, a third-party API token); user login passwords should normally be one-way verified.

## 21.5 “Should every database entry be encrypted?”

Strong viva answer: **not indiscriminately; classify data and threat model first.**

- **Disk/full-volume encryption:** protects lost physical media; transparent to DB and normally weak against a compromised running host.
- **TDE/database-at-rest encryption:** protects data files, logs, temp files, and—if configured—backups from offline theft; DB engine sees plaintext.
- **Column/field encryption in DB:** protects selected sensitive columns but may restrict indexing, joins, range search, and optimizer statistics.
- **Application/client-side envelope encryption:** DB stores ciphertext and cannot directly decrypt without external key service; stronger against a DB-only breach, but queries/constraints/search and rotation become harder.
- **Deterministic encryption:** permits equality leakage/search but reveals repeated values and frequency; use only with a justified design.

Encrypt high-impact secrets/PII where the threat warrants it; protect keys in a KMS/HSM or separated secret service; use per-data keys wrapped by rotating key-encryption keys; authenticate ciphertext with AEAD; encrypt backups and log replicas too. Hash/tokenize when reversibility is unnecessary.

## 21.6 Data in transit and operational controls

- Use TLS with certificate/hostname validation for client–DB and replication links.
- Rotate credentials, disable defaults, and avoid credentials in command lines/history. The supplied lab's `system/123` style is a teaching artifact, not production practice.
- Restrict network reachability; do not expose the DB directly to the public Internet.
- Audit authentication, DDL, privilege change, and sensitive read/write events; protect audit logs from alteration.
- Mask/synthesize production data before development use.
- Prevent inference: even aggregate/query access can leak sensitive facts through small groups or repeated differencing.

## 21.7 Integrity and availability controls

- Primary/foreign/unique/check constraints and correct transaction isolation protect integrity.
- Digital signatures/MACs detect unauthorized modification where database trust is insufficient.
- Replication/failover, rate limiting, resource quotas, backups, and capacity monitoring protect availability.
- Replication is not backup: corruption/deletion may replicate immediately.

---

# 22. Distributed Databases

> **[CORE SUPPLEMENT—source boundary]** No distributed-database unit appears in the two current merged sources. This is a compact but rigorous viva supplement.

## 22.1 Distribution choices

- **Replication:** copies the same logical data at several nodes.
- **Horizontal fragmentation/sharding:** different rows at different nodes, e.g. by customer region/hash.
- **Vertical fragmentation:** different columns at different nodes; retain a key so fragments can be losslessly rejoined.
- **Hybrid:** shard, then replicate each shard.

A good fragmentation design aims for:

- completeness: every item appears somewhere;
- reconstructability: original relation can be recovered by union/join;
- controlled disjointness: avoid unintended duplicate ownership, except deliberate key copies/replicas.

Sharding improves scale/locality but complicates cross-shard joins, global uniqueness, rebalancing, and multi-shard transactions.

## 22.2 Replication

- **Synchronous:** wait for required replicas before success; stronger durability/read freshness, higher latency/lower availability during failures.
- **Asynchronous:** primary acknowledges before replicas catch up; lower write latency, but stale reads and loss of acknowledged recent data can occur on failover.
- **Leader-based:** one writer/order source, followers replicate.
- **Multi-leader/leaderless:** greater write availability/geographic locality but conflict detection/resolution is harder.

With $N$ replicas, a simplified quorum system chooses read quorum $R$ and write quorum $W$. Conditions such as $R+W>N$ and $2W>N$ make read/write and write/write quorums overlap, but linearizability still depends on versioning, failure, membership, and protocol details—not arithmetic alone.

## 22.3 Distributed query processing

Data transfer can dominate local I/O. Push selections/projections to the data site; choose a join site; exploit partition-wise parallel joins.

A **semijoin** can reduce transfer:

1. Site R sends only `π_joinKey(R)` to site S.
2. S computes matching rows `S ⋉ keys(R)` and sends only those back.
3. R completes the join.

The extra round is worthwhile when it filters much more data than the key list costs.

## 22.4 Two-phase commit (2PC)

2PC gives atomic commit across participants; it does not by itself provide transaction isolation.

### Phase 1: prepare/vote

~~~text
coordinator -> participants: PREPARE
participant:
    validate transaction
    force prepared state/updates needed for recovery
    retain locks/resources
    reply YES or NO
~~~

### Phase 2: decide

~~~text
if every vote is YES:
    coordinator durably logs COMMIT
    sends COMMIT to all
else:
    coordinator logs/sends ABORT
participants log decision, release resources, acknowledge
~~~

After voting YES, a participant is **in doubt** and cannot unilaterally abort without risking atomicity. If the coordinator is unreachable, classical 2PC can block. Consensus-backed transaction managers and presumed-abort/commit variants improve failure handling, but CAP/availability trade-offs do not disappear.

## 22.5 Distributed deadlock

No single node may see the full wait cycle:

~~~text
at site A: T1 waits for T2
at site B: T2 waits for T1
~~~

Solutions include centralized/global wait-for graph detection, hierarchical or edge-chasing probes, timeouts, or prevention through global ordering/timestamps. Messages may be delayed and create stale (“phantom”) deadlock observations, so detection/recovery protocols need care.

## 22.6 CAP without the slogan error

During a network partition, a distributed service cannot guarantee both:

- **linearizable consistency** for every operation, and
- **availability** meaning every request to a nonfailed node receives a nonerror response,

while also tolerating the partition. CAP is not “pick any two forever,” and its C is not the C in ACID. Outside partitions, systems still trade latency, consistency, durability, and throughput; PACELC is a useful reminder of that broader trade-off.

**Eventual consistency** means replicas converge if updates cease and communication resumes, assuming conflict handling succeeds. It does not specify how stale reads may be, what clients observe meanwhile, or whether invariants survive concurrent writes.

## 22.7 Distributed viva one-liners

- **Replication versus backup:** replication serves availability/read scaling and mirrors current state—including mistakes; backup preserves recoverable historical copies.
- **Sharding versus partitioning:** sharding usually means partitions distributed across independent nodes; a DBMS can partition inside one server too.
- **2PC versus 2PL:** 2PC decides distributed atomic commit; 2PL controls conflicting concurrent access/serializability.
- **Consistency versus availability:** define the precise consistency model and failure condition; never answer with vague “CAP says choose two.”

---

# 23. SQL Capstone on the Course Product Schema

These examples are executable against the familiar `Product`/`PC`/`Laptop`/`Printer` teaching schema. Treat the displayed rows as a worked example: in a viva, derive the actual result from the instance the panel gives you.

## 23.1 Set operations

Makers producing a PC **or** laptop:

~~~sql
SELECT p.maker
FROM Product p JOIN PC x ON x.model = p.model
UNION
SELECT p.maker
FROM Product p JOIN Laptop x ON x.model = p.model
ORDER BY maker;
~~~

~~~text
A
B
C
D
E
F
G
~~~

`UNION` removes duplicates. `UNION ALL` would return one row per matching model, including repeated makers.

Makers producing **both** a PC and laptop:

~~~sql
SELECT p.maker
FROM Product p JOIN PC x ON x.model = p.model
INTERSECT
SELECT p.maker
FROM Product p JOIN Laptop x ON x.model = p.model
ORDER BY maker;
~~~

~~~text
A
B
E
~~~

## 23.2 Join, grouping, and HAVING

Count models of each type per maker:

~~~sql
SELECT maker, type, COUNT(*) AS model_count
FROM Product
GROUP BY maker, type
HAVING COUNT(*) >= 2
ORDER BY maker, type;
~~~

The key reasoning: `WHERE` cannot contain `COUNT(*)` for the group because WHERE filters input rows; HAVING filters the groups after aggregation.

Find maker and price of the most expensive PC:

~~~sql
SELECT p.maker, x.model, x.price
FROM PC x
JOIN Product p ON p.model = x.model
WHERE x.price = (SELECT MAX(price) FROM PC);
~~~

~~~text
MAKER  MODEL  PRICE
A      1001   2114
~~~

Using equality with `MAX` correctly returns ties; `ORDER BY price DESC FETCH FIRST 1 ROW ONLY` may arbitrarily return only one tied row unless `WITH TIES` is supported/used.

## 23.3 `ALL`, `NOT EXISTS`, and relational division

Laptops more expensive than **every** PC:

~~~sql
SELECT model, price
FROM Laptop
WHERE price > ALL (SELECT price FROM PC)
ORDER BY model;
~~~

~~~text
MODEL  PRICE
2001   3673
2005   2500
2010   2300
~~~

**Empty-set trap:** `x > ALL (empty set)` is TRUE; `x > ANY (empty set)` is FALSE. NULL values inside the subquery can make comparisons UNKNOWN.

Relational-division pattern—makers that have a product of every type appearing in Product:

~~~sql
SELECT DISTINCT p.maker
FROM Product p
WHERE NOT EXISTS (
    SELECT DISTINCT t.type
    FROM Product t
    WHERE NOT EXISTS (
        SELECT 1
        FROM Product q
        WHERE q.maker = p.maker
          AND q.type  = t.type
    )
);
~~~

~~~text
E
~~~

Read it aloud: choose maker p for whom there does **not** exist a product type for which there does **not** exist one of p's products. Double `NOT EXISTS` expresses “for all.”

## 23.4 Correlated subquery and equivalent join

PCs priced above the average PC price of their maker:

~~~sql
SELECT p.maker, x.model, x.price
FROM PC x
JOIN Product p ON p.model = x.model
WHERE x.price > (
    SELECT AVG(x2.price)
    FROM PC x2
    JOIN Product p2 ON p2.model = x2.model
    WHERE p2.maker = p.maker
)
ORDER BY p.maker, x.model;
~~~

The inner query is **correlated** through `p.maker`; conceptually it runs per outer maker/row, though an optimizer may decorrelate it into an aggregate join.

## 23.5 Outer join and NULL counting

Show every maker and its printer count, including makers without printers:

~~~sql
SELECT makers.maker,
       COUNT(pr.model) AS printer_count
FROM (SELECT DISTINCT maker FROM Product) makers
LEFT JOIN Product p
  ON p.maker = makers.maker
 AND p.type = 'printer'
LEFT JOIN Printer pr
  ON pr.model = p.model
GROUP BY makers.maker
ORDER BY makers.maker;
~~~

Why `COUNT(pr.model)` instead of `COUNT(*)`? A maker with no printer still has one NULL-extended outer-join row; `COUNT(*)` would count it as 1, while `COUNT(non_null_column)` ignores NULL.

Placing `p.type='printer'` in `WHERE` would reject the NULL-extended rows and accidentally turn the left join into an inner-like result. Put the preserved-side matching condition in `ON`.

## 23.6 Add the missing integrity declaratively

The supplied schema intentionally/educationally omits several relationships. A stricter product design can add:

~~~sql
ALTER TABLE Product ADD CONSTRAINT ck_product_type
CHECK (type IN ('pc', 'laptop', 'printer'));

ALTER TABLE PC ADD CONSTRAINT fk_pc_product
FOREIGN KEY (model) REFERENCES Product(model);

ALTER TABLE Laptop ADD CONSTRAINT fk_laptop_product
FOREIGN KEY (model) REFERENCES Product(model);

ALTER TABLE Printer ADD CONSTRAINT fk_printer_product
FOREIGN KEY (model) REFERENCES Product(model);
~~~

These FKs prove that a subtype model exists in Product, but they do not by themselves prove that `PC.model` points to a Product row whose `type='pc'`. Enforcing that cross-table subtype discriminator may require a redesigned composite key/unique constraint, table inheritance features, assertion (rarely supported), or trigger.

For Movie:

~~~sql
ALTER TABLE StarsIn ADD CONSTRAINT fk_starsin_movie
FOREIGN KEY (title, year) REFERENCES Movie(title, year);

ALTER TABLE StarsIn ADD CONSTRAINT fk_starsin_star
FOREIGN KEY (name) REFERENCES MovieStar(name);

ALTER TABLE Movie ADD CONSTRAINT fk_movie_studio
FOREIGN KEY (studio) REFERENCES Studio(name);
~~~

Before adding these constraints to already loaded data, find and repair orphan rows; otherwise the ALTER may fail.

---

# 24. Fast Viva Drill

## 24.1 Twenty-five direct answers

1. **Database versus DBMS?** Database is the persistent organized data; DBMS is the software controlling definition, query, update, concurrency, security, and recovery.
2. **Schema versus instance?** Schema is structure/constraints; instance is the current data state.
3. **Candidate key versus superkey?** Candidate key is a minimal superkey; a superkey may contain unnecessary attributes.
4. **Primary key versus index?** Primary key is a logical uniqueness/entity constraint; an index is a physical access structure. A DBMS often creates an index to enforce the key, but they are not the same abstraction.
5. **Foreign key?** Referencing attributes whose non-NULL values must match a referenced candidate/unique key, preserving referential integrity.
6. **NULL?** Missing/unknown/not-applicable marker, not zero or empty string; comparisons yield three-valued logic, so use `IS NULL`.
7. **WHERE versus HAVING?** WHERE filters rows before grouping; HAVING filters groups after aggregation.
8. **`COUNT(*)` versus `COUNT(A)`?** First counts rows; second counts rows where A is non-NULL.
9. **DELETE versus DROP?** DELETE removes selected rows and preserves table definition; DROP removes the schema object. TRUNCATE semantics/transaction behavior are product-specific but normally removes all rows with less row-by-row logging.
10. **View versus materialized view?** Ordinary view stores a query definition; materialized view stores its result and must be refreshed/maintained.
11. **Trigger versus procedure?** Trigger fires automatically on an event; procedure is invoked explicitly. Hidden trigger side effects should be used sparingly.
12. **Why normalize?** Remove redundancy caused by dependencies and prevent update/insert/delete anomalies.
13. **3NF versus BCNF?** BCNF requires every nontrivial FD determinant to be a superkey; 3NF also permits a non-superkey determinant when the RHS is prime. 3NF can always preserve dependencies via synthesis.
14. **Lossless versus dependency-preserving?** Lossless recreates exactly the relation after decomposition; dependency preservation enforces original FDs without rejoining.
15. **Clustered versus nonclustered index?** Clustered search-key order matches physical data order; nonclustered does not. A file can have only one primary clustering order but many secondary indexes.
16. **Why B+ tree?** High fan-out gives a shallow balanced tree; leaves contain all data entries and are linked for range scans; updates stay logarithmic.
17. **B+ tree versus hash?** Both support equality; B+ tree also supports ordered/range queries, whereas hashing has expected constant equality but no order.
18. **Why might a scan beat an index?** Predicate selects many rows, the index is unclustered, random fetches dominate, or the table is small/cached.
19. **ACID?** Atomicity, Consistency, Isolation, Durability.
20. **Serial versus serializable?** Serial has no interleaving; serializable may interleave but is equivalent to an allowed serial order.
21. **Conflict-serializability test?** Build precedence graph from ordered conflicting operations; acyclic iff conflict serializable; topological order gives serial order.
22. **2PL?** Acquire locks in a growing phase, then release in shrinking phase; guarantees conflict serializability but can deadlock.
23. **Deadlock versus starvation?** Deadlock is cyclic waiting; starvation is indefinite delay and need not contain a cycle.
24. **WAL?** Log an update durably before its dirty page and force the commit log information before acknowledging commit.
25. **2PL versus 2PC?** 2PL enforces concurrency isolation/serializability; 2PC coordinates one atomic commit decision across distributed participants.

## 24.2 Whiteboard answer templates

### Normalize a schema

~~~text
write R and FDs -> split RHS -> compute closures/keys -> mark prime attributes
-> test exact NF definition -> choose violating FD -> decompose
-> prove lossless -> test dependency preservation
~~~

### Determine whether a schedule is serializable

~~~text
list conflicting operation pairs -> orient each precedence edge
-> draw graph -> detect cycle -> if acyclic, topological order
-> separately check recoverable/cascadeless/strict if asked
~~~

### Choose an index

~~~text
predicate and order -> selectivity -> equality/range/spatial
-> clustering -> composite prefix -> covering opportunity
-> read benefit versus write/space cost
~~~

### Choose a join

~~~text
condition type -> cardinalities/pages -> memory -> indexes/order
-> estimate nested/indexed/hash/merge costs -> consider skew/output order
~~~

---

# 25. Exact Source-Coverage and Asset Audit

## 25.1 Current merged-slide coverage

The current academic folder contains two authoritative merged PDFs, and every extractable page was re-read:

| Source | Pages | Chapters represented in this volume |
|---|---:|---|
| `DBMS_Ashik_Sir_merged.pdf` | 559 | Chapters 1–11 and the logical portions of 20: architecture, SQL, relational algebra, ER/EER, dependencies, keys, normalization, constraints and views |
| `DBMS_Toufiq_Sir_merged.pdf` | 337 | Chapters 12–19 and the physical/transaction portions of 20: storage, file organization, indexes, query execution/optimization, transactions, schedules and concurrency control |
| **Total** | **896** | **all current DBMS slide pages routed** |

Important figures—ER mappings, B+ tree operations, record layouts, join plans, precedence graphs, lock schedules and snapshot-isolation anomalies—are explained in words and worked traces so they can be reproduced on a whiteboard.

## 25.2 Scope boundary

The old folder contained individual decks, product/movie archives and loader logs; those are no longer the selected academic sources. Their stale file-by-file audit has therefore been removed. Recovery, database security and distributed-database material remain clearly labeled **[CORE SUPPLEMENT]** because they are standard viva topics even where the two merged decks give them little or no depth.
## 25.3 Corrections and supplements ledger

- SQL's conceptual result model in the lectures is related to mathematical relations, but ordinary SQL query blocks use bag semantics unless duplicate elimination is requested.
- `PRIMARY KEY` is not synonymous with “primary/clustering index.”
- `NULL = NULL` is UNKNOWN, not TRUE; use `IS NULL`.
- `NOT IN` with a NULL-producing subquery can become UNKNOWN; correlated `NOT EXISTS` is often safer for anti-join logic.
- Natural join is valid algebra/SQL but fragile when schemas evolve; explicit join predicates are safer in production.
- The design deck centers 1NF/BCNF; 2NF, 3NF synthesis, canonical cover, 4NF/5NF were added and labeled.
- The concurrency material emphasizes locks/2PL and snapshot isolation; timestamps, validation, granularity and other multiversion mechanisms are retained as labeled supplements where the merged slides give less depth.
- Recovery, advanced database security and distributed DBMS are explicitly marked standard-core supplements where the current merged slides do not cover them deeply.
- Product/version claims and hardware rates in slides are historical examples; the enduring mechanism is stated separately.

# 26. Workbook interview case — migrate a document database to SQL

**Source:** BRAC Ques Bank C41. The DB sheet itself says only “Work in progress”;
it is not evidence that DBMS is unimportant. The full SQL, indexing, ACID,
normalization, concurrency and recovery material above remains essential.

Suppose a document stores:

```json
{"order_id": 9, "customer": {"id": 2, "name": "Rina"},
 "items": [{"sku": "P1", "qty": 2, "unit_price": 120},
           {"sku": "P2", "qty": 1, "unit_price": 50}]}
```

Do not simply replace JSON syntax with a `CREATE TABLE`. Identify entities,
relationships, keys, constraints and which values are historical snapshots.

```text
Customer 1 ---- many OrderHeader 1 ---- many OrderLine many ---- 1 Product
customer_id         order_id               (order_id, line_no)    sku
```

```sql
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE Product (
    sku VARCHAR(40) PRIMARY KEY
);
CREATE TABLE OrderHeader (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(customer_id)
);
CREATE TABLE OrderLine (
    order_id INTEGER REFERENCES OrderHeader(order_id),
    line_no INTEGER,
    sku VARCHAR(40) NOT NULL REFERENCES Product(sku),
    qty INTEGER NOT NULL CHECK (qty > 0),
    unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, line_no)
);
```

Keep `unit_price` on the line if it records the price **at purchase**; joining
to the product's current price would rewrite history. `line_no` preserves array
order and permits repeated SKUs. Use stable source IDs or an explicit mapping
table, and decide how missing fields, explicit nulls, type inconsistencies,
duplicate customers and unknown referenced products will be handled.

The example order total is $2\cdot120+1\cdot50=290$:

```sql
SELECT order_id, SUM(qty * unit_price) AS total
FROM OrderLine
GROUP BY order_id;
```

Migration sequence: profile data → agree on schema/mapping → stage and validate
→ load in dependency order → reconcile → catch up concurrent changes → cut
over with a rollback plan. Reconcile counts, distinct keys, foreign-key orphans,
totals and sampled records; order count alone does not prove line-item fidelity.
Use idempotent batch keys so retries do not duplicate orders. For a live system,
design a write pause or coordinated change-data capture; uncontrolled dual writes
can diverge. SQL versus NoSQL does not by itself decide whether transactions,
joins or consistency are supported; inspect the actual product/model.

## 26.1 Demo and follow-up questions

For a 4–5 minute demo, draw the single document, extract the four entities,
show the 1:N relationships, and calculate the total. Save full production
migration detail for Q&A. Expected follow-ups: why a composite key? Why keep
price on the line? How to preserve nested-array order? What validates migration?
How can a retry be safe? Which operation must be atomic?

# 27. Final self-test

Before the viva, you should be able to do these without looking:

1. compute attribute closure and every candidate key;
2. derive a canonical cover and perform a lossless BCNF/3NF decomposition;
3. map weak entity, multivalued attribute, 1:N, M:N, and ISA from ER to relations;
4. write a join/group/subquery/anti-join and predict NULL/duplicate behavior;
5. trace B+ tree search, split, borrow, merge, and height cost;
6. calculate one external-sort and block/hash-join I/O cost;
7. estimate equality and equijoin cardinalities from $n,b,V$;
8. build a precedence graph and state serial order or cycle;
9. distinguish recoverable, cascadeless, strict, 2PL, SI, and serializable;
10. explain WAL, STEAL/NO-FORCE, checkpoint, REDO, and UNDO;
11. answer exactly why encrypting every DB column is not automatically best;
12. distinguish RAID/replication/backup, and 2PL/2PC.
