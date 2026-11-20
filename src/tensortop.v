
`default_nettype none

module tensortop (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] data_in,
    input  wire [1:0] cmd,
    input  wire [2:0] index,
    input  wire       status_sel,
    output reg  [7:0] data_out
);

    // Four operand bytes:
    // A column 0, B row 0, A column 1, B row 1
    reg [7:0] operand0, operand1;
    reg [7:0] operand2, operand3;

    localparam IDLE = 2'd0;
    localparam RUN0 = 2'd1;
    localparam RUN1 = 2'd2;
    localparam DONE = 2'd3;

    reg [1:0] state;

    wire start;
    wire mac_clear;
    wire mac_enable;

    assign start = (cmd == 2'b10) &&
                   ((state == IDLE) || (state == DONE));

    assign mac_clear  = start;
    assign mac_enable = (state == RUN0) ||
                        (state == RUN1);

    // Select appropriate operands for each cycle
    wire [7:0] a_byte =
        (state == RUN1) ? operand2 : operand0;

    wire [7:0] b_byte =
        (state == RUN1) ? operand3 : operand1;

    wire signed [11:0] c00, c01, c10, c11;

    matrix_core core (
        .clk(clk),
        .rst_n(rst_n),
        .clear(mac_clear),
        .enable(mac_enable),
        .a0(a_byte[3:0]),
        .a1(a_byte[7:4]),
        .b0(b_byte[3:0]),
        .b1(b_byte[7:4]),
        .c00(c00),
        .c01(c01),
        .c10(c10),
        .c11(c11)
    );

    // Controller and operand storage
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            operand0 <= 0;
            operand1 <= 0;
            operand2 <= 0;
            operand3 <= 0;
        end else begin
            case (state)
                IDLE, DONE: begin
                    if (start) begin
                        state <= RUN0;
                    end else if (cmd == 2'b01) begin
                        case (index)
                            3'd0: operand0 <= data_in;
                            3'd1: operand1 <= data_in;
                            3'd2: operand2 <= data_in;
                            3'd3: operand3 <= data_in;
                            default: ;
                        endcase
                    end
                end

                RUN0: state <= RUN1;
                RUN1: state <= DONE;

                default: state <= IDLE;
            endcase
        end
    end

    // Read results through an 8-bit output port.
    // Each signed 12-bit result uses two indices.
    always @(*) begin
        if (status_sel) begin
            data_out = {6'b0,
                        (state == RUN0 || state == RUN1),
                        (state == DONE)};
        end else begin
            case (index)
                3'd0: data_out = c00[7:0];
                3'd1: data_out =
                    {{4{c00[11]}}, c00[11:8]};
                3'd2: data_out = c01[7:0];
                3'd3: data_out =
                    {{4{c01[11]}}, c01[11:8]};
                3'd4: data_out = c10[7:0];
                3'd5: data_out =
                    {{4{c10[11]}}, c10[11:8]};
                3'd6: data_out = c11[7:0];
                3'd7: data_out =
                    {{4{c11[11]}}, c11[11:8]};
                default: data_out = 0;
            endcase
        end
    end

endmodule

`default_nettype wire
