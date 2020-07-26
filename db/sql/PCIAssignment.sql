CREATE trigger trig_pciassignment ON pciassignment
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT sector_id FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT assign_id, earfcn, sector_id, sector_name, enodeb_id,
    pci, pss, sss, longitude, latitude, style, opt_datetime FROM inserted
    OPEN cur  --打开游标
    DECLARE @assign_id SMALLINT
    DECLARE @earfcn INT
    DECLARE @sector_id NVARCHAR(50)
    DECLARE @sector_name NVARCHAR(200)
    DECLARE @enodeb_id INT
    DECLARE @pci INT
    DECLARE @pss INT
    DECLARE @sss INT
    DECLARE @longitude FLOAT
    DECLARE @latitude FLOAT
    DECLARE @style VARCHAR(50)
    DECLARE @opt_datetime NVARCHAR(50)
    FETCH NEXT FROM cur INTO @assign_id, @earfcn, @sector_id, @sector_name, @enodeb_id,
    @pci, @pss, @sss, @longitude, @latitude, @style, @opt_datetime
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM pciassignment WHERE assign_id=@assign_id AND sector_id=@sector_id)<1)
        BEGIN
            INSERT INTO pciassignment VALUES (@assign_id, @earfcn, @sector_id, @sector_name,
            @enodeb_id, @pci, @pss, @sss, @longitude, @latitude, @style, @opt_datetime)
        END
        ELSE
        BEGIN
            UPDATE pciassignment SET
            earfcn=@earfcn,
            sector_name=@sector_name,
            enodeb_id=@enodeb_id,
            pci=@pci,
            pss=@pss,
            sss=@sss,
            longitude=@longitude,
            latitude=@latitude,
            style=@style,
            opt_datetime=@opt_datetime
            WHERE sector_id=@sector_id AND assign_id=@assign_id
        END
        FETCH NEXT FROM cur INTO @assign_id, @earfcn, @sector_id, @sector_name, @enodeb_id,
        @pci, @pss, @sss, @longitude, @latitude, @style, @opt_datetime   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END