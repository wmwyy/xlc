using System;
using System.Collections.Generic;
using System.Linq;

namespace GateCalculator.Services;

public static class Calculators
{
    public static A01Result ComputeA01(A01Input input)
    {
        if (input.H0 <= 0 || input.H <= 0) throw new ArgumentException("H0 和 H 必须大于 0");
        if (input.N <= 0) throw new ArgumentException("孔数 N 必须大于 0");
        if (input.b0 <= 0 || input.b1 <= 0) throw new ArgumentException("b0 和 b1 必须大于 0");

        var ratio = input.h1 / input.H0;
        var sigma = 2.31 * Math.Pow(ratio * (1 - ratio), 0.4);

        double epsilonC = double.NaN;
        double epsilonB = double.NaN;
        double epsilon;

        if (input.SingleHole || input.N == 1)
        {
            epsilon = 1 - 0.171 * (1 - input.b0 / input.b1) * Math.Sqrt(input.b0 / input.b1);
        }
        else
        {
            epsilonC = 1 - 0.171 * (1 - input.b0 / (input.b0 + input.dc)) * Math.Sqrt(input.b0 / (input.b0 + input.dc));
            var dbTerm = input.b0 + input.db / 2.0;
            epsilonB = 1 - 0.171 * (1 - input.b0 / dbTerm) * Math.Sqrt(input.b0 / dbTerm);
            epsilon = epsilonC * (input.N - 1.0) / input.N + epsilonB / input.N;
        }

        var denominator = sigma * epsilon * input.m * Math.Sqrt(2 * input.g) * Math.Pow(input.H, 1.5);
        if (denominator <= 0) throw new ArgumentException("分母为 0，请检查输入");

        var b0Total = input.Q / denominator;
        return new A01Result(b0Total, sigma, epsilon, epsilonC, epsilonB);
    }

    public static A02Result ComputeA02(A02Input input)
    {
        if (input.H0 <= 0) throw new ArgumentException("H0 必须大于 0");
        var headDiff = input.H0 - input.h0;
        if (headDiff <= 0) throw new ArgumentException("(H0 - h0) 必须大于 0");

        var mu0 = 0.877 + Math.Pow(input.hs / input.H0 - 0.65, 2);
        var denominator = input.sigma * mu0 * Math.Sqrt(2 * input.g * headDiff);
        if (denominator <= 0) throw new ArgumentException("分母为 0，请检查输入");

        var b0Total = input.Q / denominator;
        return new A02Result(b0Total, mu0);
    }

    public static A03Result ComputeA03(A03Input input)
    {
        if (input.H0 <= 0 || input.H <= 0 || input.he <= 0) throw new ArgumentException("H0、H、he 必须大于 0");
        var ratio = (input.he - input.hc) / (input.H - input.hc);
        var sigmaPrime = LookupSigmaPrime(ratio);

        var lambda = 0.4 / Math.Pow(Math.E, Math.Pow(Math.Log(6 * input.epsilonC), 2));
        var epsilonPrime = 1.0 / (1.0 + Math.Sqrt(lambda * (1 - Math.Pow(input.he / input.H, 2))));
        var mu = input.phi * Math.Exp(epsilonPrime) / Math.Sqrt(1 - epsilonPrime * input.he / input.H);

        var denominator = sigmaPrime * mu * input.he * Math.Sqrt(2 * input.g * input.H0);
        if (denominator <= 0) throw new ArgumentException("分母为 0，请检查输入");

        var b0Total = input.Q / denominator;
        return new A03Result(b0Total, sigmaPrime, mu, epsilonPrime, lambda);
    }

    private static double LookupSigmaPrime(double ratio)
    {
        var table = TableA03;
        if (ratio <= table.First().Ratio) return table.First().Value;
        if (ratio >= table.Last().Ratio) return table.Last().Value;

        for (var i = 0; i < table.Count - 1; i++)
        {
            var a = table[i];
            var b = table[i + 1];
            if (ratio >= a.Ratio && ratio <= b.Ratio)
            {
                var t = (ratio - a.Ratio) / (b.Ratio - a.Ratio);
                return a.Value + t * (b.Value - a.Value);
            }
        }

        return table.Last().Value;
    }

    private static readonly List<TablePoint> TableA03 = new()
    {
        new TablePoint(0.000, 0.02),
        new TablePoint(0.100, 0.05),
        new TablePoint(0.200, 0.10),
        new TablePoint(0.300, 0.16),
        new TablePoint(0.400, 0.21),
        new TablePoint(0.500, 0.27),
        new TablePoint(0.550, 0.30),
        new TablePoint(0.600, 0.36),
        new TablePoint(0.650, 0.42),
        new TablePoint(0.700, 0.49),
        new TablePoint(0.750, 0.56),
        new TablePoint(0.800, 0.63),
        new TablePoint(0.850, 0.70),
        new TablePoint(0.900, 0.78),
        new TablePoint(0.920, 0.86),
        new TablePoint(0.930, 0.94),
        new TablePoint(0.940, 1.02),
        new TablePoint(0.950, 1.10),
        new TablePoint(0.960, 1.18),
        new TablePoint(0.980, 1.26),
        new TablePoint(0.995, 1.30)
    };
}

public record A01Input(double Q, double H0, double H, double h1, double b0, double b1, int N, double dc, double db, double m, double g, bool SingleHole);
public record A01Result(double B0, double Sigma, double Epsilon, double EpsilonC, double EpsilonB);

public record A02Input(double Q, double H0, double h0, double hs, double sigma, double g);
public record A02Result(double B0, double Mu0);

public record A03Input(double Q, double H0, double H, double he, double hc, double epsilonC, double phi, double g);
public record A03Result(double B0, double SigmaPrime, double Mu, double EpsilonPrime, double Lambda);

public record TablePoint(double Ratio, double Value);
