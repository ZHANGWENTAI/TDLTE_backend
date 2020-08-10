IF EXISTS(SELECT NAME FROM sys.indexes WHERE NAME = 'index_cell_sector_name')
    DROP INDEX index_cell_sector_name ON cell;
CREATE NONCLUSTERED INDEX  index_cell_sector_name ON cell(sector_name)
IF EXISTS(SELECT NAME FROM sys.indexes WHERE NAME = 'index_cell_enodebid')
    DROP INDEX index_cell_enodebid ON cell;
CREATE NONCLUSTERED INDEX  index_cell_enodebid ON cell(enodeb_id)
IF EXISTS(SELECT NAME FROM sys.indexes WHERE NAME = 'index_cell_enodeb_name')
    DROP INDEX index_cell_enodeb_name ON cell;
CREATE NONCLUSTERED INDEX  index_cell_enodeb_name ON cell(enodeb_name)
