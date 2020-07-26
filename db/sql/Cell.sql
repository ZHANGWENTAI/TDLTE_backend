CREATE trigger trig_cell ON cell
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT sector_id FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT city, sector_id, sector_name, enodebid, enode_name,
    earfcn, pci, pss, sss, tac, azimuth, height,
    electtilt, mechtilt, totletilt FROM inserted
    OPEN cur  --打开游标
    DECLARE @city NVARCHAR(255)
    DECLARE @sector_id NVARCHAR(255)
    DECLARE @sector_name NVARCHAR(255)
    DECLARE @enodebid INT
    DECLARE @enode_name NVARCHAR(255)
    DECLARE @earfcn INT
    DECLARE @pci INT
    DECLARE @pss INT
    DECLARE @sss INT
    DECLARE @tac INT
    DECLARE @azimuth FLOAT
    DECLARE @height FLOAT
    DECLARE @electtilt FLOAT
    DECLARE @mechtilt FLOAT
    DECLARE @totletilt FLOAT
    FETCH NEXT FROM cur INTO @city, @sector_id, @sector_name, @enodebid, @enode_name,
    @earfcn, @pci, @pss, @sss, @tac, @azimuth, @height, @electtilt, @mechtilt, @totletilt
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM cell WHERE sector_id=@sector_id)<1)
        BEGIN
            IF ((SELECT COUNT (*) FROM enodeb WHERE enodebid=@enodebid)>=1)
            BEGIN
                INSERT INTO cell VALUES (@city, @sector_id, @sector_name,
                @enodebid, @enode_name,@earfcn, @pci, @pss, @sss, @tac,
                @azimuth, @height, @electtilt, @mechtilt, @totletilt)
            END
        END
        ELSE
        BEGIN
            UPDATE cell SET
            city=@city,
            sector_name=@sector_name,
            enodebid=@enodebid,
            enode_name=@enode_name,
            earfcn=@earfcn,
            pci=@pci,
            pss=@pss,
            sss=@sss,
            tac=@tac,
            azimuth=@azimuth,
            height=@height,
            electtilt=@electtilt,
            mechtilt=@mechtilt,
            totletilt=@totletilt
            WHERE sector_id=@sector_id
        END
        FETCH NEXT FROM cur INTO @city, @sector_id, @sector_name, @enodebid, @enode_name,
        @earfcn, @pci, @pss, @sss, @tac, @azimuth, @height,
        @electtilt, @mechtilt, @totletilt   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END