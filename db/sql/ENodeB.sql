CREATE trigger trig_enodeb ON enodeb
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT enodebid FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT city, enodebid, enodeb_name, vendor, longitude, latitude, style FROM inserted
    OPEN cur  --打开游标
    DECLARE @city NVARCHAR(255)
    DECLARE @enodebid INT
    DECLARE @enodeb_name NVARCHAR(255)
    DECLARE @vendor NVARCHAR(255)
    DECLARE @longitude FLOAT
    DECLARE @latitude FLOAT
    DECLARE @style NVARCHAR(255)
    FETCH NEXT FROM cur INTO @city, @enodebid, @enodeb_name, @vendor, @longitude, @latitude, @style
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM enodeb WHERE enodebid=@enodebid)<1)
        BEGIN
            INSERT INTO enodeb VALUES (@city, @enodebid, @enodeb_name, @vendor, @longitude, @latitude, @style)
        END
        ELSE
        BEGIN
            UPDATE enodeb SET
            city=@city,
            enodeb_name=@enodeb_name,
            vendor=@vendor,
            longitude=@longitude,
            latitude=@latitude,
            style=@style
            WHERE enodebid=@enodebid
        END
        FETCH NEXT FROM cur INTO @city, @enodebid, @enodeb_name, @vendor, @longitude, @latitude, @style   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END