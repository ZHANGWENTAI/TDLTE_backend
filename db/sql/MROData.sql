CREATE trigger trig_mrodata ON mrodata
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT time_stamp FROM inserted)  --插入和更新
    DECLARE cur CURSOR forward_only
    FOR SELECT * FROM inserted
    OPEN cur  --打开游标
    DECLARE @time_stamp NVARCHAR(30)
    DECLARE @serving_sector NVARCHAR(50)
    DECLARE @interfering_sector NVARCHAR(50)
    DECLARE @lte_sc_rsrp FLOAT
    DECLARE @lte_nc_rsrp FLOAT
    DECLARE @lte_nc_earfcn INT
    DECLARE @lte_nc_pci SMALLINT
    FETCH NEXT FROM cur INTO @time_stamp, @serving_sector, @interfering_sector,
    @lte_sc_rsrp, @lte_nc_rsrp, @lte_nc_earfcn, @lte_nc_pci
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
        IF ((SELECT COUNT (*) FROM mrodata WHERE time_stamp=@time_stamp AND
        serving_sector=@serving_sector AND interfering_sector=@interfering_sector)<1)
        BEGIN
            INSERT INTO mrodata VALUES (@time_stamp, @serving_sector, @interfering_sector,
            @lte_sc_rsrp, @lte_nc_rsrp, @lte_nc_earfcn, @lte_nc_pci)
        END
        ELSE
        BEGIN
            UPDATE mrodata SET
            lte_sc_rsrp=@lte_sc_rsrp,
            lte_nc_rsrp=@lte_nc_rsrp,
            lte_nc_earfcn=@lte_nc_earfcn,
            lte_nc_pci=@lte_nc_pci
            WHERE time_stamp=@time_stamp AND serving_sector=@serving_sector AND
            interfering_sector=@interfering_sector
        END
        FETCH NEXT FROM cur INTO @time_stamp, @serving_sector, @interfering_sector,
        @lte_sc_rsrp, @lte_nc_rsrp, @lte_nc_earfcn, @lte_nc_pci   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END