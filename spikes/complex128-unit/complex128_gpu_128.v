`timescale 1ns/1ps
module complex128_gpu_128 (
    input  wire [8191:0] a_re,
    input  wire [8191:0] a_im,
    input  wire [8191:0] b_re,
    input  wire [8191:0] b_im,
    input  wire          op,
    output wire [8191:0] r_re,
    output wire [8191:0] r_im
);
    genvar i;
    generate
        for (i = 0; i < 128; i = i + 1) begin : lanes
            complex128_unit lane (
                .a_re(a_re[i*64 +: 64]),
                .a_im(a_im[i*64 +: 64]),
                .b_re(b_re[i*64 +: 64]),
                .b_im(b_im[i*64 +: 64]),
                .op(op),
                .r_re(r_re[i*64 +: 64]),
                .r_im(r_im[i*64 +: 64])
            );
        end
    endgenerate
endmodule
