CREATE trigger trig_optcell ON optcell
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT sector_id FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only FOR SELECT sector_id, earfcn, cell_type FROM inserted
    OPEN cur  --打开游标
    DECLARE @sector_id NVARCHAR(50)
    DECLARE @earfcn INT
    DECLARE @cell_type NVARCHAR(50)
    FETCH NEXT FROM cur INTO @sector_id, @earfcn, @cell_type
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM optcell WHERE sector_id=@sector_id)<1)
        BEGIN
            INSERT INTO optcell VALUES (@sector_id, @earfcn, @cell_type)
        END
        ELSE
        BEGIN
            UPDATE optcell SET
            earfcn=@earfcn,
            cell_type=@cell_type
            WHERE sector_id=@sector_id
        END
        FETCH NEXT FROM cur INTO @sector_id, @earfcn, @cell_type   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END