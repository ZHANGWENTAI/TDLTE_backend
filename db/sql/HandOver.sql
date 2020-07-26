CREATE trigger trig_handover ON handover
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT city FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT * FROM inserted
    OPEN cur  --打开游标
    DECLARE @city NVARCHAR(255)
    DECLARE @scell_id VARCHAR(50)
    DECLARE @ncell_id VARCHAR(50)
    DECLARE @hoatt INT
    DECLARE @hosucc INT
    DECLARE @hosuccrate FLOAT
    FETCH NEXT FROM cur INTO @city, @scell_id, @ncell_id, @hoatt, @hosucc, @hosuccrate
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF (@hosuccrate='3.1415926') BEGIN SET @hosuccrate=null END
        IF ((SELECT COUNT (*) FROM handover WHERE scell_id=@scell_id AND ncell_id=@ncell_id)<1)
        BEGIN
            INSERT INTO handover VALUES (@city, @scell_id, @ncell_id, @hoatt, @hosucc, @hosuccrate)
        END
        ELSE
        BEGIN
            UPDATE handover SET
            city=@city,
            hoatt=@hoatt,
            hosucc=@hosucc,
            hosuccrate=@hosuccrate
            WHERE scell_id=@scell_id AND ncell_id=@ncell_id
        END
        FETCH NEXT FROM cur INTO @city, @scell_id, @ncell_id, @hoatt, @hosucc, @hosuccrate   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END