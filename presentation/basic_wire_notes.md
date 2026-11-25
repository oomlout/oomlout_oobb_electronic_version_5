# Basic wire holder render notes

AI-generated CAD illustrations. These assemblies have not been physically fit-tested.

- The printed body is the existing basic 3 × 3, 4 mm production STL. Its front pocket is 15.64 × 3.48 mm and its housing channel is 8.02 mm wide. No printed geometry is changed by the header correction.
- The connector uses **header_long**, with equal exposed pin ends. The reference is HOAUC **1625-1140CNG0S150001**, [LCSC C343639](https://www.lcsc.com/product-detail/C343639.html). The manufacturer drawing HYC-1812011115 gives 2.54 mm pitch, 0.64 mm square pins, a 2.5 mm insulator, 6.25 mm exposed at each end and 15 mm overall pin length. It lists 1–40 positions. [LCSC-hosted drawing](https://atta.szlcsc.com/upload/public/pdf/source/20260917/9F655738B2D4F4FC500A9931BECCBD77.pdf).
- C343639 is the 40-position purchasing reference. Shorter generic header_long records are cut sections, not separate verified LCSC listings. The complete plastic strip remains intact after pins 1, 2 and 6 are pushed out of the six-position basic section.
- The earlier asymmetric Harwin PCB-header geometry remains in the separate standard header catalogue. It is not used by any header_oobb model or assembly view.
- The [Harwin M20-1060300](https://www.harwin.com/products/M20-1060300) housing and [M20-1180046](https://www.harwin.com/products/M20-1180046) sockets remain the DuPont-style housing/contact references. The housing is 7.82 × 14 × 2.50 mm. Loose socket wings are shown before crimping; cavities, bevels, grooves and wire bends are illustrative where feature dimensions are unavailable.
- The basic header remains centred at Y=−14.28 mm: its front tip is now Y=−21.78 mm, 0.22 mm inside the plate front. The rear end enters the housing by approximately 6.23 mm. Header and housing pin axes remain at Z=2.47 mm.
- `basic_wire.json` and the per-part `assembly.json` record source hashes, render paths and quantities. Update the base README thumbnail with `python presentation/scripts/build_project_thumbnails.py --filter electronic-parts` in the base repository.
