CREATE trigger trig_atuc2i ON atuc2i INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT sector_id FROM inserted)  --插入和更新
DECLARE cur CURSOR forward_only
FOR SELECT * FROM inserted
OPEN cur  --打开游标
DECLARE @sector_id NVARCHAR(50)
DECLARE @ncell_id NVARCHAR(50)
DECLARE @ratio_all FLOAT
DECLARE @rank INT
DECLARE @cosite TINYINT
FETCH NEXT FROM cur INTO @sector_id, @ncell_id, @ratio_all, @rank, @cosite
WHILE(@@FETCH_STATUS=0)
BEGIN
    --增加操作
    IF ((SELECT COUNT (*) FROM atuc2i WHERE sector_id=@sector_id AND ncell_id=@ncell_id)<1)
    BEGIN
        INSERT INTO atuc2i VALUES (@sector_id, @ncell_id, @ratio_all, @rank, @cosite)
    END
    ELSE
    BEGIN
        UPDATE atuc2i SET
        ratio_all=@ratio_all,
        rank=@rank,
        cosite=@cosite
        WHERE sector_id=@sector_id AND ncell_id=@ncell_id
    END
    FETCH NEXT FROM cur INTO @sector_id, @ncell_id, @ratio_all, @rank, @cosite   --指向下一条
END
CLOSE cur  --关闭游标
DEALLOCATE cur  --销毁游标资源
END