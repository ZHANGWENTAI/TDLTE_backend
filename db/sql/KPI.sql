CREATE trigger trig_kpi ON kpi
INSTEAD OF INSERT
AS
BEGIN
IF EXISTS(SELECT enb_name FROM inserted)
    DECLARE cur CURSOR forward_only FOR select * FROM inserted
    OPEN cur
    DECLARE @time_stamp NVARCHAR(10)
    DECLARE @enb_name NVARCHAR(50)
    DECLARE @sector_name VARCHAR(50)
    DECLARE @rrc_conn_succ_rate FLOAT
    DECLARE @erab_succ_rate FLOAT
    DECLARE @erab_drop_rate FLOAT
    DECLARE @wireless_conn FLOAT
    DECLARE @wireless_drop FLOAT
    DECLARE @enb_inter FLOAT
    DECLARE @enb_outer FLOAT
    DECLARE @same_freq_handover FLOAT
    DECLARE @diff_freq_handover FLOAT
    DECLARE @handover_rate FLOAT
    DECLARE @pdcp_upper BIGINT
    DECLARE @pdcp_down BIGINT
    DECLARE @rrc_rebuild FLOAT
    DECLARE @enb_handout_succ INT
    DECLARE @enb_handout_req INT
    FETCH NEXT FROM cur INTO
    @time_stamp, @enb_name, @sector_name,
    @rrc_conn_succ_rate,
    @erab_succ_rate,
    @erab_drop_rate,
    @wireless_conn,
    @wireless_drop,
    @enb_inter,
    @enb_outer,
    @same_freq_handover,
    @diff_freq_handover,
    @handover_rate,
    @pdcp_upper,
    @pdcp_down,
    @rrc_rebuild,
    @enb_handout_succ,
    @enb_handout_req
    WHILE(@@FETCH_STATUS=0)
    BEGIN
        --增加操作
    IF ((SELECT COUNT (*) FROM kpi WHERE enb_name=@enb_name AND time_stamp=@time_stamp AND sector_name=@sector_name)<1)
    BEGIN
        INSERT INTO kpi VALUES (@time_stamp, @enb_name, @sector_name,
        @rrc_conn_succ_rate,
        @erab_succ_rate,
        @erab_drop_rate,
        @wireless_conn,
        @wireless_drop,
        @enb_inter,
        @enb_outer,
        @same_freq_handover,
        @diff_freq_handover,
        @handover_rate,
        @pdcp_upper,
        @pdcp_down,
        @rrc_rebuild,
        @enb_handout_succ,
        @enb_handout_req)
    END
    ELSE
    BEGIN
        UPDATE kpi SET
            rrc_conn_succ_rate=@rrc_conn_succ_rate,
            erab_succ_rate=@erab_succ_rate,
            erab_drop_rate=@erab_drop_rate,
            wireless_conn=@wireless_conn,
            wireless_drop=@wireless_drop,
            enb_inter=@enb_inter,
            enb_outer=@enb_outer,
            same_freq_handover=@same_freq_handover,
            diff_freq_handover=@diff_freq_handover,
            handover_rate=@handover_rate,
            pdcp_upper=@pdcp_upper,
            pdcp_down=@pdcp_down,
            rrc_rebuild=@rrc_rebuild,
            enb_handout_succ=@enb_handout_succ,
            enb_handout_req=@enb_handout_req
            WHERE enb_name=@enb_name AND time_stamp=@time_stamp AND sector_name=@sector_name
        END
        FETCH NEXT FROM cur INTO  @enb_name, @time_stamp, @sector_name,
        @rrc_conn_succ_rate,
        @erab_succ_rate,
        @erab_drop_rate,
        @wireless_conn,
        @wireless_drop,
        @enb_inter,
        @enb_outer,
        @same_freq_handover,
        @diff_freq_handover,
        @handover_rate,
        @pdcp_upper,
        @pdcp_down,
        @rrc_rebuild,
        @enb_handout_succ,
        @enb_handout_req   --指向下一条
    END
    CLOSE cur  --关闭游标
    DEALLOCATE cur  --销毁游标资源
END