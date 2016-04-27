defmodule CloudflareApiTools do
  use HTTPoison.Base

  @expected_fields ~w(result success errors messages)

  def main(args) do
    args
    |> parse_args
    |> process
  end

  defp parse_args(args) do
    # {options, _, _} = OptionParser.parse(args,
    #   switches: [zone: :string])

    # options
    options = OptionParser.parse(args, switches: [help: :boolean,
                                                  zone: :string,
                                                  clearcache: :string,
                                                  devmode: :string])

    case options do
      {[zone: zone], _, _} -> {:zone, zone}
      {[clearcache: clearcache], _, _} -> {:clearcache, clearcache}
      {[devmode: devmode], _, _} -> {:devmode, devmode}
      {[help: true], _, _} -> :help
      _ -> :help
    end
  end

  def process({:zone, zone}) do
    IO.puts "Got zone: #{zone}"
  end

  def process({:devmode, devmode}) do
    IO.puts "Got devmode: #{devmode}"
  end

  def process({:clearcache, clearcache}) do
    
    IO.puts "Got clearcache: #{clearcache}"
  end

  def process(:help) do
    IO.puts """
Usage: ./cf [OPTION]... -z [DOMAIN]
Manage common Cloudflare tasks via their API.
Example: ./cf -d on -z example.com

Options:
-h, --help\t\tShow this help message
-z, --zone DOMAIN\tApply action to DOMAIN.
-d, --devmode STATUS\tTurn dev mode on or off. STATUS can be 'on' or 'off'.
-c, --clearcache\tClear the cache
    """
  end

end
