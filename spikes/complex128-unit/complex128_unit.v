`timescale 1ns/1ps
module complex128_unit (
    input  wire [63:0] a_re,
    input  wire [63:0] a_im,
    input  wire [63:0] b_re,
    input  wire [63:0] b_im,
    input  wire        op,   // 0 = add, 1 = multiply
    output reg  [63:0] r_re,
    output reg  [63:0] r_im
);
    wire signed [63:0] ar = $signed(a_re);
    wire signed [63:0] ai = $signed(a_im);
    wire signed [63:0] br = $signed(b_re);
    wire signed [63:0] bi = $signed(b_im);

    always @(*) begin
        if (op == 1'b0) begin
            r_re = ar + br;
            r_im = ai + bi;
        end else begin
            r_re = (ar * br) - (ai * bi);
            r_im = (ar * bi) + (ai * br);
        end
    end
endmodule
