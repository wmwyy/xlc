using System;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using GateCalculator.Services;
using System.IO;

namespace GateCalculator;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        Loaded += (_, _) => LoadDiagramImages();
    }

    private void LoadDiagramImages()
    {
        SetImageSource(A01Img, "A01.png");
        SetImageSource(A02Img, "A02.png");
        SetImageSource(A03Img, "A03.png");
    }

    private void SetImageSource(Image img, string fileName)
    {
        try
        {
            var baseDir = AppContext.BaseDirectory;
            var path = Path.Combine(baseDir, "Assets", fileName);
            if (!File.Exists(path)) return;
            var bmp = new BitmapImage();
            bmp.BeginInit();
            bmp.UriSource = new Uri(path, UriKind.Absolute);
            bmp.CacheOption = BitmapCacheOption.OnLoad;
            bmp.EndInit();
            img.Source = bmp;
        }
        catch
        {
            // ignore load failures
        }
    }

    private void OnScaleChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
    {
        if (sender is Slider slider)
        {
            var scale = e.NewValue;
            switch (slider.Tag)
            {
                case "A01":
                    A01ScaleTransform.ScaleX = scale;
                    A01ScaleTransform.ScaleY = scale;
                    break;
                case "A02":
                    A02ScaleTransform.ScaleX = scale;
                    A02ScaleTransform.ScaleY = scale;
                    break;
                case "A03":
                    A03ScaleTransform.ScaleX = scale;
                    A03ScaleTransform.ScaleY = scale;
                    break;
            }
        }
    }

    private void OnFillA01Sample(object sender, RoutedEventArgs e)
    {
        A01Q.Text = "120";
        A01H0.Text = "8";
        A01H.Text = "10";
        A01h1.Text = "5";
        A01b0.Text = "3";
        A01b1.Text = "3.5";
        A01N.Text = "1";
        A01dc.Text = "0";
        A01db.Text = "0";
        A01m.Text = "0.885";
        A01g.Text = "9.81";
        A01Single.IsChecked = true;
    }

    private void OnFillA02Sample(object sender, RoutedEventArgs e)
    {
        A02Q.Text = "150";
        A02H0.Text = "8";
        A02h0.Text = "2";
        A02hs.Text = "5";
        A02sigma.Text = "0.82";
        A02g.Text = "9.81";
    }

    private void OnFillA03Sample(object sender, RoutedEventArgs e)
    {
        A03Q.Text = "180";
        A03H0.Text = "9";
        A03H.Text = "10";
        A03he.Text = "4";
        A03hc.Text = "1.5";
        A03epsilonC.Text = "0.2";
        A03phi.Text = "0.96";
        A03g.Text = "9.81";
    }

    private void OnCalcA01(object sender, RoutedEventArgs e)
    {
        try
        {
            var input = new A01Input(
                Q: ReadDouble(A01Q),
                H0: ReadDouble(A01H0),
                H: ReadDouble(A01H),
                h1: ReadDouble(A01h1),
                b0: ReadDouble(A01b0),
                b1: ReadDouble(A01b1),
                N: ReadInt(A01N, 1),
                dc: ReadDouble(A01dc),
                db: ReadDouble(A01db),
                m: ReadDouble(A01m, 0.885),
                g: ReadDouble(A01g, 9.81),
                SingleHole: A01Single.IsChecked == true
            );

            var r = Calculators.ComputeA01(input);
            A01Result.Text =
                $"B0 = {r.B0:F4} m\n" +
                $"sigma = {r.Sigma:F4}, epsilon = {r.Epsilon:F4}\n" +
                $"epsilon_c = {(double.IsNaN(r.EpsilonC) ? "--" : r.EpsilonC.ToString("F4"))}, " +
                $"epsilon_b = {(double.IsNaN(r.EpsilonB) ? "--" : r.EpsilonB.ToString("F4"))}";
        }
        catch (Exception ex)
        {
            A01Result.Text = "输入有误: " + ex.Message;
        }
    }

    private void OnCalcA02(object sender, RoutedEventArgs e)
    {
        try
        {
            var input = new A02Input(
                Q: ReadDouble(A02Q),
                H0: ReadDouble(A02H0),
                h0: ReadDouble(A02h0),
                hs: ReadDouble(A02hs),
                sigma: ReadDouble(A02sigma, 1.0),
                g: ReadDouble(A02g, 9.81)
            );

            var r = Calculators.ComputeA02(input);
            A02Result.Text = $"B0 = {r.B0:F4} m； mu0 = {r.Mu0:F4}";
        }
        catch (Exception ex)
        {
            A02Result.Text = "输入有误: " + ex.Message;
        }
    }

    private void OnCalcA03(object sender, RoutedEventArgs e)
    {
        try
        {
            var input = new A03Input(
                Q: ReadDouble(A03Q),
                H0: ReadDouble(A03H0),
                H: ReadDouble(A03H),
                he: ReadDouble(A03he),
                hc: ReadDouble(A03hc),
                epsilonC: ReadDouble(A03epsilonC),
                phi: ReadDouble(A03phi, 0.97),
                g: ReadDouble(A03g, 9.81)
            );

            var r = Calculators.ComputeA03(input);
            A03Result.Text =
                $"B0 = {r.B0:F4} m\n" +
                $"sigma' = {r.SigmaPrime:F4}, mu = {r.Mu:F4}\n" +
                $"epsilon' = {r.EpsilonPrime:F4}, lambda = {r.Lambda:F4}";
        }
        catch (Exception ex)
        {
            A03Result.Text = "输入有误: " + ex.Message;
        }
    }

    private static double ReadDouble(TextBox box, double? fallback = null)
    {
        var text = box.Text?.Trim();
        if (double.TryParse(text, NumberStyles.Float, CultureInfo.InvariantCulture, out var v)) return v;
        if (double.TryParse(text, NumberStyles.Float, CultureInfo.CurrentCulture, out v)) return v;
        if (fallback.HasValue) return fallback.Value;
        throw new ArgumentException("请输入数值: " + (box.Name ?? ""));
    }

    private static int ReadInt(TextBox box, int fallback)
    {
        var text = box.Text?.Trim();
        if (int.TryParse(text, NumberStyles.Integer, CultureInfo.InvariantCulture, out var v)) return v;
        if (int.TryParse(text, NumberStyles.Integer, CultureInfo.CurrentCulture, out v)) return v;
        return fallback;
    }
}
