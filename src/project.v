
`default_nettype none

module tt_um_muhamm30_tinytensor (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    tensortop accelerator (
        .clk(clk),
        .rst_n(rst_n),
        .data_in(ui_in),
        .cmd(uio_in[1:0]),
        .index(uio_in[4:2]),
        .status_sel(uio_in[5]),
        .data_out(uo_out)
    );

    // Bidirectional pins are inputs only
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire _unused = &{ena, uio_in[7:6], 1'b0};

endmodule

`default_nettype wire
