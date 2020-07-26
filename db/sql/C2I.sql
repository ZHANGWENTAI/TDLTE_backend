CREATE trigger trig_c2i
ON c2i
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT city FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT * FROM inserted
    OPEN cur  --打开游标
    DECLARE @city NVARCHAR(255)
    DECLARE @scell_id NVARCHAR(255)
    DECLARE @ncell_id NVARCHAR(255)
    DECLARE @prc2i9 FLOAT
    DECLARE @c2i_mean FLOAT
    DECLARE @std FLOAT
    DECLARE @samplecount FLOAT
    DECLARE @weightedc2i FLOAT
    FETCH NEXT FROM cur INTO @city, @scell_id, @ncell_id, @prc2i9, @c2i_mean, @std, @samplecount, @weightedc2i
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM c2i WHERE scell_id=@scell_id AND ncell_id=@ncell_id)<1)
        BEGIN
            INSERT INTO c2i VALUES (@city, @scell_id, @ncell_id, @prc2i9, @c2i_mean, @std, @samplecount, @weightedc2i)
        END
        ELSE
        BEGIN
            UPDATE c2i SET
            city=@city,
            prc2i9=@prc2i9,
            c2i_mean=@c2i_mean,
            std=@std,
            samplecount=@samplecount,
            weightedc2i=@weightedc2i
            WHERE scell_id=@scell_id AND ncell_id=@ncell_id
        END
        FETCH NEXT FROM cur INTO @city, @scell_id, @ncell_id, @prc2i9, @c2i_mean, @std, @samplecount, @weightedc2i   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END