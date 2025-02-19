<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
</script>



<footer class="footerbg footer text-stone-100 p-10">
    <nav>
      <h6 class="footer-title">Company</h6>
      <a href="/" class="link link-hover">About us</a>
      <a href="/" class="link link-hover">Contact</a>
      <a href="/" class="link link-hover">Jobs</a>
    </nav>
    <nav>
      <h6 class="footer-title">Legal</h6>
      <a href="/" class="link link-hover">Terms of use</a>
      <a href="/" class="link link-hover">Privacy policy</a>
      <a href="/" class="link link-hover">Cookie policy</a>
    </nav>
    <form>
        <h6 class="footer-title">Newsletter</h6>
        <fieldset class="form-control w-80">
          <!-- svelte-ignore a11y_label_has_associated_control -->
          <label class="label">
            <span class="label-text text-stone-100">Enter your email address</span>
          </label>
          <div class="join">
            <Input type="email" placeholder="email" class="bg-white border-gray-300 text-black max-w-[200px] mr-2"/>

                <Button class="rounded-xl bg-white text-black px-5 py-4 text-md mr-3 hover:bg-stone-200">
                    Subscribe
                </Button>

    
          </div>
        </fieldset>
      </form>
  </footer>


<style>
.footerbg{
    background-color: rgb(20, 20, 20);
}
</style>