`timescale 1ns/1ps
module complex128_gpu_128_tb;
    reg  [8191:0] a_re, a_im, b_re, b_im;
    reg           op;
    wire [8191:0] r_re, r_im;

    integer i;
    integer errors = 0;
    reg signed [63:0] ar, ai, br, bi;
    reg signed [63:0] expected_re, expected_im;

    complex128_gpu_128 dut (
        .a_re(a_re), .a_im(a_im), .b_re(b_re), .b_im(b_im),
        .op(op), .r_re(r_re), .r_im(r_im)
    );

    task check_lane(input integer lane, input signed [63:0] exp_re,
                    input signed [63:0] exp_im);
        begin
            if (($signed(r_re[lane*64 +: 64]) !== exp_re) ||
                ($signed(r_im[lane*64 +: 64]) !== exp_im)) begin
                $display("FAIL lane=%0d op=%0d got=(%0d,%0d) expected=(%0d,%0d)",
                         lane, op,
                         $signed(r_re[lane*64 +: 64]),
                         $signed(r_im[lane*64 +: 64]), exp_re, exp_im);
                errors = errors + 1;
            end
        end
    endtask

    initial begin
        a_re = '0;
        a_im = '0;
        b_re = '0;
        b_im = '0;
        op = 1'b0;

        // a=(i-4)+(2i+1)j, b=(3-i)+(i-5)j.
        for (i = 0; i < 128; i = i + 1) begin
            ar = i - 4;
            ai = 2*i + 1;
            br = 3 - i;
            bi = i - 5;
            a_re[i*64 +: 64] = ar;
            a_im[i*64 +: 64] = ai;
            b_re[i*64 +: 64] = br;
            b_im[i*64 +: 64] = bi;
        end

        #1;
        for (i = 0; i < 128; i = i + 1) begin
            expected_re = -1;
            expected_im = 3*i - 4;
            check_lane(i, expected_re, expected_im);
        end

        op = 1'b1;
        #1;
        for (i = 0; i < 128; i = i + 1) begin
            // Hand-expanded products, independent of the DUT expression.
            expected_re = -3*i*i + 16*i - 7;
            expected_im = -i*i - 4*i + 23;
            check_lane(i, expected_re, expected_im);
        end

        // Signed maximum plus one wraps to signed minimum.
        a_re = '0;
        a_im = '0;
        b_re = '0;
        b_im = '0;
        a_re[63:0] = 64'h7fff_ffff_ffff_ffff;
        b_re[63:0] = 64'd1;
        op = 1'b0;
        #1;
        check_lane(0, 64'h8000_0000_0000_0000, 64'd0);

        if (errors != 0)
            $fatal(1, "FAIL: %0d lane checks failed", errors);
        $display("PASS: 128 parallel complex lanes");
        $finish;
    end
endmodule
