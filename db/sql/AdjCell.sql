CREATE trigger trig_adjcell
ON adjcell
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT s_sector_id FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only FOR SELECT s_sector_id, n_sector_id, s_earfcn, n_earfcn FROM inserted
    OPEN cur  --打开游标
    DECLARE @s_sector_id VARCHAR(255)
    DECLARE @n_sector_id VARCHAR(255)
    DECLARE @s_earfcn INT
    DECLARE @n_earfcn INT
    FETCH NEXT FROM cur INTO @s_sector_id, @n_sector_id, @s_earfcn, @n_earfcn
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM adjcell WHERE s_sector_id=@s_sector_id AND n_sector_id=@n_sector_id)<1)
        BEGIN
            INSERT INTO adjcell VALUES (@s_sector_id, @n_sector_id, @s_earfcn, @n_earfcn)
        END
        ELSE
        BEGIN
            UPDATE adjcell SET
            s_earfcn=@s_earfcn,
            n_earfcn=@n_earfcn
            WHERE s_sector_id=@s_sector_id AND n_sector_id=@n_sector_id
        END
        FETCH NEXT FROM cur INTO @s_sector_id, @n_sector_id, @s_earfcn, @n_earfcn   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END