CREATE trigger trig_atuhandover ON atuhandover
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT s_sector_id FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT * FROM inserted
    OPEN cur  --打开游标
    DECLARE @s_sector_id NVARCHAR(50)
    DECLARE @n_sector_id NVARCHAR(50)
    DECLARE @hoatt INT
    FETCH NEXT FROM cur INTO @s_sector_id, @n_sector_id, @hoatt
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM atuhandover WHERE s_sector_id=@s_sector_id AND n_sector_id=@n_sector_id)<1)
        BEGIN
            INSERT INTO atuhandover VALUES (@s_sector_id, @n_sector_id, @hoatt)
        END
        ELSE
        BEGIN
            UPDATE atuhandover SET
            hoatt=@hoatt
            WHERE s_sector_id=@s_sector_id AND n_sector_id=@n_sector_id
        END
        FETCH NEXT FROM cur INTO @s_sector_id, @n_sector_id, @hoatt   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END